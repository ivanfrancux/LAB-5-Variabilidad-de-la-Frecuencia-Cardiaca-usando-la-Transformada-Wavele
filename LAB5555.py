import threading
import serial
import struct
import numpy as np
import csv
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.signal import butter, lfilter
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QComboBox, QFileDialog, QMessageBox, QSlider
)
from serial.tools import list_ports


class SignalEmitter(QObject):
    update_plot = pyqtSignal(np.ndarray)


class Principal(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECG Signal Viewer")
        self.resize(800, 600)
        self.duracion = 15  # duración visible en segundos
        self.fm = 1000
        self.muestras_totales = int(self.duracion * self.fm)

        # Inicializa las otras variables
        self.x = np.linspace(0, self.duracion, self.muestras_totales)
        self.y = np.zeros(self.muestras_totales)
        self.buffer_guardado = []

        # Llama a la función init_ui después de inicializar las variables
        self.init_ui()
        self.puertos_disponibles()

        self.ser1 = None
        self.hilo_serial = None
        self.lectura_activa = False

        # Gráfico
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        self.line, = self.ax.plot(self.x, self.y, color='b')
        self.ax.set_xlabel('Tiempo (s)')
        self.ax.set_ylabel('Amplitud')
        self.ax.set_title('Señal ECG en Tiempo Real')
        self.ax.grid(True)

        # Filtro IIR
        self.fc_baja = 0.5
        self.fc_alta = 45
        self.fn_baja = self.fc_baja / (0.5 * self.fm)
        self.fn_alta = self.fc_alta / (0.5 * self.fm)
        self.orden_filtro = 2  # Orden del filtro IIR
        self.b, self.a = butter(self.orden_filtro, [self.fn_baja, self.fn_alta], btype='band')

        # Señales
        self.signal_emitter = SignalEmitter()
        self.signal_emitter.update_plot.connect(self.actualizar_grafico)

        # Inicializamos el slider con un valor predeterminado
        self.slider_value = 0

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.puertos = QComboBox()
        self.layout.addWidget(QLabel("Puertos disponibles:"))
        self.layout.addWidget(self.puertos)

        self.connect = QPushButton("CONECTAR")
        self.connect.clicked.connect(self.conectar)
        self.layout.addWidget(self.connect)

        self.save_btn = QPushButton("Guardar")
        self.save_btn.clicked.connect(self.guardar_datos)
        self.layout.addWidget(self.save_btn)

        self.load_btn = QPushButton("Cargar")  # Botón de carga
        self.load_btn.clicked.connect(self.cargar_archivo)
        self.layout.addWidget(self.load_btn)

        # Crear slider solo después de inicializar muestras_totales
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setValue(0)
        self.slider.setTickInterval(1000)
        self.slider.valueChanged.connect(self.actualizar_slider)
        self.layout.addWidget(self.slider)

    def puertos_disponibles(self):
        for port in list_ports.comports():
            self.puertos.addItem(port.device)

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

    def conectar(self):
        estado = self.connect.text()
        if estado == "CONECTAR":
            com = self.puertos.currentText()
            try:
                self.ser1 = serial.Serial(com, 115200, timeout=1)
                self.lectura_activa = True
                self.hilo_serial = threading.Thread(target=self.leer_datos_serial)
                self.hilo_serial.start()
                self.connect.setText("DESCONECTAR")
                print("Puerto conectado")
            except serial.SerialException as e:
                self.mostrar_error(f"Error al conectar: {e}")
        else:
            self.lectura_activa = False
            if self.hilo_serial:
                self.hilo_serial.join()
            if self.ser1:
                self.ser1.close()
            self.connect.setText("CONECTAR")
            print("Puerto desconectado")

    def leer_datos_serial(self):
        while self.lectura_activa and self.ser1 and self.ser1.is_open:
            try:
                data = self.ser1.read(100)
                if len(data) == 100:
                    data = struct.unpack('100B', data)
                    for i in range(0, len(data), 2):
                        if i + 1 < len(data):
                            raw = (data[i] << 8) | data[i + 1]
                            self.y = np.roll(self.y, -1)
                            self.y[-1] = raw
                            self.buffer_guardado.append(raw)
                            # Limitar a 5 minutos de datos (300000 muestras)
                            if len(self.buffer_guardado) > 300000:
                                self.buffer_guardado.pop(0)

                    # Filtrar con el filtro IIR
                    filtrado = lfilter(self.b, self.a, self.y)

                    self.signal_emitter.update_plot.emit(filtrado)

            except Exception as e:
                print(f"Error en lectura serial: {e}")
                break

    def actualizar_grafico(self, datos):
        self.line.set_ydata(datos)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def guardar_datos(self):
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar ECG", "", "CSV (*.csv)")
        if not archivo:
            return
        try:
            with open(archivo, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Muestras"])
                for v in self.buffer_guardado:
                    writer.writerow([v])
            print(f"Datos guardados en {archivo}")
        except Exception as e:
            self.mostrar_error(f"Error al guardar: {e}")

    def cargar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar archivo ECG", "", "CSV (*.csv)")
        if not archivo:
            return
        try:
            with open(archivo, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Saltar encabezado
                datos = [float(row[0]) for row in reader]

            # Guardamos todos los datos cargados en el buffer
            self.buffer_guardado = datos

            # Establecer el máximo del slider según la cantidad de muestras
            self.slider.setMaximum(len(self.buffer_guardado) - self.muestras_totales)

            # Cargar los primeros datos y mostrarlos
            datos_iniciales = datos[:self.muestras_totales]
            filtrado = lfilter(self.b, self.a, np.array(datos_iniciales))
            self.signal_emitter.update_plot.emit(filtrado)

            print(f"Archivo cargado: {archivo}")
        except Exception as e:
            self.mostrar_error(f"Error al cargar archivo: {e}")

    def actualizar_slider(self):
        # Obtener el valor del slider y actualizar el gráfico con las muestras correspondientes
        offset = self.slider.value()
        datos_muestra = self.buffer_guardado[offset:offset + self.muestras_totales]

        # Asegurarse de que los datos a mostrar tengan la longitud correcta
        if len(datos_muestra) < self.muestras_totales:
            padding = [0] * (self.muestras_totales - len(datos_muestra))
            datos_muestra = padding + datos_muestra

        filtrado = lfilter(self.b, self.a, np.array(datos_muestra))
        self.signal_emitter.update_plot.emit(filtrado)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ventana = Principal()
    ventana.show()
    sys.exit(app.exec_())


