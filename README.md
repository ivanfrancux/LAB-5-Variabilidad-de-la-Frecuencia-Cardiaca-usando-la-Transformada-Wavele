# LAB-5- Variabilidad de la Frecuencia Cardiaca usando la Transformada Wavelet
## Introdución 
En esta práctica de laboratorio se llevó a cabo la captura de un electrocardiograma (ECG), así como su posterior preprocesamiento, con el objetivo de analizar en profundidad las características de la señal cardíaca. Un aspecto fundamental de este estudio fue el análisis de la variabilidad de la frecuencia cardíaca (HRV), un parámetro clave para evaluar el funcionamiento del sistema nervioso autónomo y la salud cardiovascular en general. Para ello, se empleó la transformada wavelet, una herramienta matemática que permite identificar cambios en las frecuencias características de la señal y analizar su dinámica temporal con alta precisión.

## Teoria  
Actividad simpática y parasimpática del sistema nervioso autónomo,
Efecto de la actividad simpática y parasimpática en la frecuencia
cardiaca,
- Variabilidad de la frecuencia cardiaca (HRV) medida como fluctuaciones
en el intervalo R-R, y las frecuencias de interés en este análisis,
- Transformada Wavelet: definición, usos y tipos de wavelet utilizadas en
señales biológicas.
relacionados con el SNA, la HRV y la transformada wavelet



## Características de la señal adquirida
Para la adquisición de la señal electrocardiográfica (ECG), se utilizó una tarjeta de adquisición de datos NI DAQ-6004; la cual ofrece una resolución de 12 bits, equivalente a 4096 niveles de cuantización. La frecuencia de muestreo se configuró en 800 Hz, un valor significativamente superior al mínimo requerido por el teorema de Nyquist. Dado que las señales cardíacas típicas se encuentran en un rango de 0.05 Hz a 100 Hz, una frecuencia de muestreo de al menos 200 Hz habría sido suficiente para evitar aliasing. Sin embargo, se optó por un muestreo más alta para  así garantizar una mayor precisión en la captura de detalles transitorios y mejorar la calidad de la señal.

En esta primera etapa del experimento, se realizó la captura de la señal ECG en reposo, registrando las variaciones de voltaje asociadas a la actividad eléctrica del corazón. Esta señal fue procesada para eliminar artefactos, ruido y componentes no deseados, permitiendo un análisis más detallado de las características fisiológicas relevantes.
![image](https://github.com/user-attachments/assets/1b0464ad-2829-4870-ba29-a9d0bba600c6)

```pyton

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

```
```pyton

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
```
```pyton
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
```

![image](https://github.com/user-attachments/assets/e3f4b30a-2f1d-4aaa-9260-9e9389b1a12a)


## Diagrama de flujo
Se elaboro un diagrama  donde podrmos conocer el expliciatamente cómo llevarán a cabo el proyecto, las técnicas y herramientas que van a utilizar y los resultados que vana obtener
Anexo 

