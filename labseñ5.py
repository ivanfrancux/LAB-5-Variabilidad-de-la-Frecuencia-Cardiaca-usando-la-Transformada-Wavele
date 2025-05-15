import threading  
import serial
import struct
import numpy as np
import csv
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.signal import butter, lfilter, find_peaks
import pywt
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFileDialog, QMessageBox, QSlider, QPushButton
)

class SignalEmitter(QObject):
    update_plot = pyqtSignal(object)  # Para pasar tupla (datos, x)

class Principal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECG Signal Viewer")
        self.resize(1200, 700)

        # Parámetros de duración
        self.duracion_total = 300  # 5 minutos
        self.duracion_ventana = 60  # Mostrar 1 minuto
        self.fm = 1000  # Frecuencia de muestreo (Hz)
        self.muestras_ventana = int(self.duracion_ventana * self.fm)

        self.buffer_guardado = []

        self.init_ui()
        self.init_plot()
        self.init_filter()

        self.signal_emitter = SignalEmitter()
        self.signal_emitter.update_plot.connect(self.actualizar_grafico)

    def init_ui(self):
        self.layout_principal = QVBoxLayout(self)

        self.load_btn = QPushButton("Cargar")
        self.load_btn.clicked.connect(self.cargar_archivo)
        self.layout_principal.addWidget(self.load_btn)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setValue(0)
        self.slider.setTickInterval(self.fm * 5)  # Marcas cada 5 segundos
        self.slider.setSingleStep(self.fm)  # Avance de 1 segundo
        self.slider.valueChanged.connect(self.actualizar_slider)
        self.layout_principal.addWidget(self.slider)

        # Layout para los gráficos wavelet y bandas lado a lado
        self.layout_graficos = QHBoxLayout()
        self.layout_principal.addLayout(self.layout_graficos)

        # Aquí se añadirán los canvas de wavelet y bandas

    def init_plot(self):
        # Canvas para ECG arriba
        self.fig_ecg = Figure(figsize=(12, 3))
        self.canvas_ecg = FigureCanvas(self.fig_ecg)
        self.layout_principal.insertWidget(2, self.canvas_ecg)

        self.ax_ecg = self.fig_ecg.add_subplot(111)
        self.line_ecg, = self.ax_ecg.plot([], [], color='b')
        self.line_picos, = self.ax_ecg.plot([], [], "ro", markersize=4)
        self.ax_ecg.set_title('ECG')
        self.ax_ecg.set_xlabel('Tiempo (s)')
        self.ax_ecg.set_ylabel('Amplitud')
        self.ax_ecg.grid(True)

        # Canvas para wavelet
        self.fig_wavelet = Figure(figsize=(6, 4))
        self.canvas_wavelet = FigureCanvas(self.fig_wavelet)
        self.layout_graficos.addWidget(self.canvas_wavelet)

        self.ax_wavelet = self.fig_wavelet.add_subplot(111)
        self.ax_wavelet.set_title("Transformada Wavelet Morlet")
        self.ax_wavelet.set_ylabel("Escalas")
        self.ax_wavelet.set_xlabel("Tiempo (s)")

        # Canvas para bandas de potencia
        self.fig_bandas = Figure(figsize=(6, 4))
        self.canvas_bandas = FigureCanvas(self.fig_bandas)
        self.layout_graficos.addWidget(self.canvas_bandas)

        self.ax_bandas = self.fig_bandas.add_subplot(111)
        self.ax_bandas.set_title("Potencia en bandas de frecuencia (Baja y Alta)")
        self.ax_bandas.set_xlabel("Tiempo (s)")
        self.ax_bandas.set_ylabel("Potencia")
        self.ax_bandas.grid(True)

    def init_filter(self):
        fc_baja = 0.5
        fc_alta = 45
        fn_baja = fc_baja / (0.5 * self.fm)
        fn_alta = fc_alta / (0.5 * self.fm)
        orden = 2
        self.b, self.a = butter(orden, [fn_baja, fn_alta], btype='band')

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

    def cargar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar archivo ECG", "", "CSV (*.csv)")
        if not archivo:
            return
        try:
            with open(archivo, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Saltar encabezado
                datos = [float(row[0]) for row in reader]

            self.buffer_guardado = datos
            max_slider = max(0, len(self.buffer_guardado) - self.muestras_ventana)
            self.slider.setMaximum(max_slider)
            self.actualizar_slider()
            print(f"Archivo cargado: {archivo}")
        except Exception as e:
            self.mostrar_error(f"Error al cargar archivo: {e}")

    def actualizar_slider(self):
        offset = self.slider.value()
        datos_muestra = self.buffer_guardado[offset:offset + self.muestras_ventana]
        if len(datos_muestra) < self.muestras_ventana:
            datos_muestra = [0] * (self.muestras_ventana - len(datos_muestra)) + datos_muestra
        filtrado = lfilter(self.b, self.a, np.array(datos_muestra))
        x_offset = offset / self.fm
        x_din = np.linspace(x_offset, x_offset + self.duracion_ventana, self.muestras_ventana)
        self.signal_emitter.update_plot.emit((filtrado, x_din))

    def actualizar_grafico(self, datos_yx):
        datos, x_din = datos_yx
        self.line_ecg.set_data(x_din, datos)
        self.x = x_din  # Actualizar eje x dinámicamente
        self.ax_ecg.relim()
        self.ax_ecg.autoscale_view()
        self.actualizar_picos(datos)
        self.actualizar_wavelet_y_bandas(datos)
        self.canvas_ecg.draw()
        self.canvas_wavelet.draw()
        self.canvas_bandas.draw()

    def actualizar_picos(self, datos):
        picos, _ = find_peaks(datos, height=0.5, distance=300)
        self.line_picos.set_data(self.x[picos], datos[picos])

        rr_intervals = np.diff(picos) / self.fm
        if rr_intervals.size:
            print(f"Media RR: {np.mean(rr_intervals):.4f} s, Desv. Estándar: {np.std(rr_intervals):.4f} s")

    def actualizar_wavelet_y_bandas(self, datos):
        self.ax_wavelet.clear()
        self.ax_bandas.clear()

        self.ax_wavelet.set_title("Transformada Wavelet Morlet")
        self.ax_wavelet.set_ylabel("Escalas")
        self.ax_wavelet.set_xlabel("Tiempo (s)")

        self.ax_bandas.set_title("Potencia en bandas de frecuencia (Baja y Alta)")
        self.ax_bandas.set_xlabel("Tiempo (s)")
        self.ax_bandas.set_ylabel("Potencia")
        self.ax_bandas.grid(True)

        # CWT
        scales = np.arange(1, 201)  # Escalas hasta 200
        coef, freqs = pywt.cwt(datos, scales, 'cmor1.5-1.0', sampling_period=1/self.fm)

        # Mostrar mapa wavelet
        self.ax_wavelet.imshow(
            np.abs(coef),
            extent=[self.x[0], self.x[-1], scales.min(), scales.max()],
            cmap='jet',
            aspect='auto',
            origin='lower'
        )

        # Definir bandas en frecuencia
        banda_baja = (freqs >= 0.5) & (freqs <= 5)
        banda_alta = (freqs > 5) & (freqs <= 45)

        # Calcular potencia (magnitud al cuadrado) promedio en cada banda para cada instante temporal
        potencia_baja = np.mean(np.abs(coef[banda_baja, :])**2, axis=0)
        potencia_alta = np.mean(np.abs(coef[banda_alta, :])**2, axis=0)

        # Graficar potencias en bandas
        self.ax_bandas.plot(self.x, potencia_baja, label='Baja frecuencia (0.5-5 Hz)', color='blue')
        self.ax_bandas.plot(self.x, potencia_alta, label='Alta frecuencia (5-45 Hz)', color='red')
        self.ax_bandas.legend()

        # Análisis crítico simple (impresión)
        cambio_baja = potencia_baja.max() - potencia_baja.min()
        cambio_alta = potencia_alta.max() - potencia_alta.min()
        print(f"Cambio potencia banda baja: {cambio_baja:.3f}")
        print(f"Cambio potencia banda alta: {cambio_alta:.3f}")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ventana = Principal()
    ventana.show()
    sys.exit(app.exec_())









