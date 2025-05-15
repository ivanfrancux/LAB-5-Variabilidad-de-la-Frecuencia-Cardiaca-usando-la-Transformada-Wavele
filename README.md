# LAB-5- Variabilidad de la Frecuencia Cardiaca usando la Transformada Wavelet
## Introdución 
En esta práctica de laboratorio se llevó a cabo la captura de un electrocardiograma (ECG), así como su posterior preprocesamiento, con el objetivo de analizar en profundidad las características de la señal cardíaca. Un aspecto fundamental de este estudio fue el análisis de la variabilidad de la frecuencia cardíaca (HRV), un parámetro clave para evaluar el funcionamiento del sistema nervioso autónomo y la salud cardiovascular en general. Para ello, se empleó la transformada wavelet, una herramienta matemática que permite identificar cambios en las frecuencias características de la señal y analizar su dinámica temporal con alta precisión.

## Conceptos previos de análisis del Sistema Nervioso Autónomo mediante HRV y Transformada Wavelet
El Sistema Nervioso Autónomo regula funciones vitales como la frecuencia cardíaca, siendo clave en la Variabilidad de la Frecuencia Cardíaca (HRV); el cual es un indicador de salud cardiovascular que  se evidencia en las variaciones en los intervalos del ciclo cardiaco. Un mayor HRV indica un SNA equilibrado, mientras que una reducción puede asociarse a estrés o patologías .

El Sistema Nervioso Autónomo (SNA) regula funciones vitales como la frecuencia cardíaca, desempeñando un papel fundamental en la Variabilidad de la Frecuencia Cardíaca (HRV). Este parámetro, que cuantifica las variaciones en los intervalos del ciclo cardíaco (R-R), constituye un importante indicador de salud cardiovascular. Valores elevados de HRV reflejan un equilibrio adecuado del SNA, mientras que su disminución puede asociarse a condiciones de estrés o diversas patologías cardíacas. Para su análisis, la Transformada Wavelet es una herramienta importante puesto que permite descomponer la señal ECG en diferentes componentes frecuenciales, identificando patrones temporales y espectrales que métodos tradicionales (como la FFT) podrían pasar por alto. Esto facilita la detección de alteraciones en el dominio del tiempo-frecuencia, ofreciendo una visión más completa de la dinámica cardíaca y su relación con el SNA.
![image](https://github.com/user-attachments/assets/25b2aa97-2656-469d-9434-57fb6d3c9407)


Para el desarrollo de este trabajo se utilizo una wavelwet tipo morlet la cual nos permite descomponer la señal ECG en sus componentes frecuenciales e identificar patrones temporales y espectrales complejos. El componente de baja frecuencia (LF, 0.04-0.15 Hz), que refleja predominantemente la actividad simpática modulada por los barorreflejos, y la banda de alta frecuencia (HF, 0.15-0.4 Hz), asociada a la influencia parasimpática y sincronizada con la respiración. El cociente LF/HF cuantifica el equilibrio autonómico, donde valores elevados sugieren predominio simpático, mientras que valores reducidos indican mayor tono vagal, proporcionando así información clínicamente relevante sobre la regulación cardiovascular.  Sirve para evaluar el equilibrio entre el sistema simpático y parasimpático. 

![image](https://github.com/user-attachments/assets/b8b23c58-225d-49c5-9a56-25c0050524bc)



## Características de la señal adquirida
Para la adquisición de la señal electrocardiográfica (ECG), se utilizó una tarjeta de adquisición de datos NI DAQ-6004; la cual ofrece una resolución de 12 bits, equivalente a 4096 niveles de cuantización. La frecuencia de muestreo se configuró en 800 Hz, un valor significativamente superior al mínimo requerido por el teorema de Nyquist. Dado que las señales cardíacas típicas se encuentran en un rango de 0.05 Hz a 100 Hz, una frecuencia de muestreo de al menos 200 Hz habría sido suficiente para evitar aliasing. Sin embargo, se optó por un muestreo más alta para  así garantizar una mayor precisión en la captura de detalles transitorios y mejorar la calidad de la señal. El tiempo de muestreo utilizado es de 1.25 milisegundos entre cada muestra

En esta primera etapa del experimento, se realizó la captura de la señal ECG en reposo, registrando las variaciones de voltaje asociadas a la actividad eléctrica del corazón. Esta señal esta de manera cruda por ende podemos ver picos por fuera de lo esperado y con ruido.
![image](https://github.com/user-attachments/assets/1b0464ad-2829-4870-ba29-a9d0bba600c6)

A continuación se evidencia el codigo utilizado para la conexcion el codigo completo se encuentra en los archivos 
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
En esta interfaz bos podremos deslizar con slider por toda la muestra de 5 minutos, donde podremos identificar todas la caracteristicas de nuestra señal 

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

    # Señales
    self.signal_emitter = SignalEmitter()
    self.signal_emitter.update_plot.connect(self.actualizar_grafico)

    # Inicializamos el slider con un valor predeterminado
    self.slider_value = 0
```
Por ultimo tenemos nuestra función de guardar nuestros datos con el objetivo para poder hacer el procesamiento de la señal para su procesamiento para eliminar artefactos, ruido y componentes no deseados, permitiendo un análisis más detallado de las características fisiológicas relevantes.
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
## Procesamientio
En esta segunda parte del codigo podemos visuzalizar los estadísticos principales, así como tambien el HRV 

```pyton

```
se toma apartir del.......


Se toma un filtro tipo IIR (Filtro Digital de Respuesta Infinita al Impulso) el cual en señales electrocardiográficas (ECG) permite eliminar ruidos y artefactos que interfieren con la correcta interpretación de la señal, sin dañar las características importantes del ECG. Este tipo de filtro ayuda a eliminar interferencias de baja frecuencia, como la deriva de línea base causada por movimientos o respiración, y ruidos de alta frecuencia, como interferencias eléctricas y actividad muscular (EMG). Al filtrar estas componentes indeseadas, se mejora la calidad de la señal y se facilita la detección precisa de eventos cardíacos como los complejos QRS, ondas P y T.  Aparte son eficientes a nivel computacionales, permitiendo un procesamiento en tiempo real con un bajo costo computacional. Para el diseño en  nuestro trabajo se toma en los rangos de una frecuencia baja de 0.5  Hz y la frecuencia de 45 Hz. 

```pyton

```
A continuación se evidenciara la forma d e la creación  de la ventena asi como las graficas para el ánalisis de las frecuencias
```pyton

```

#### Usuario normal
![image](https://github.com/user-attachments/assets/27c27547-166e-49a9-97af-c10b6e22f081)
![image](https://github.com/user-attachments/assets/88fc8745-a2b6-40f3-83ff-2427891b4ebc)

![image](https://github.com/user-attachments/assets/32d3b45d-116c-4a15-9c6b-60060598d13c)

 Y se toma un espectrograma por medio de wavelet en este caso morlet gracias a esto podemos analizar la potencia de nuestra señal respecto tambien se dan graficas para el analisis que se ralizará despúes del usurio estresado.
#### Usuario estresado
![image](https://github.com/user-attachments/assets/b0c69052-0581-4693-9b7f-19fbeb9963ef)
![image](https://github.com/user-attachments/assets/e514a960-dbaa-4efb-b7dc-a9487a805e7d)

![image](https://github.com/user-attachments/assets/ccbd07a0-5309-4617-920b-1a4460a891d0)


Como podemos evidenciar se revisan respecto las frecuencias y en comprativa se logra evidenciar unos cambios clave entre  esos tenemos 
## Anexo: Diagrama de flujo y preprocesamiento de la señal


Se elaboro un diagrama  donde podrmos conocer el expliciatamente cómo llevarán a cabo el proyecto, las técnicas y herramientas que van a utilizar y los resultados que vana obtener
Anexo 

Describe completamente el diseño de los filtros utilizados con todos sus parámetros, y justifica adecuadamente su elección.
