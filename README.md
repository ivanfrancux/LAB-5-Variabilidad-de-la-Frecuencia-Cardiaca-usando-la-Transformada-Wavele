# LAB-5- Variabilidad de la Frecuencia Cardiaca usando la Transformada Wavelet
## Introducción 
En esta práctica de laboratorio se llevó a cabo la captura de un electrocardiograma (ECG), así como su posterior preprocesamiento, con el objetivo de analizar en profundidad las características de la señal cardíaca. Un aspecto fundamental de este estudio fue el análisis de la variabilidad de la frecuencia cardíaca (HRV), un parámetro clave para evaluar el funcionamiento del sistema nervioso autónomo y la salud cardiovascular en general. Para ello, se empleó la transformada wavelet, una herramienta matemática que permite identificar cambios en las frecuencias características de la señal y analizar su dinámica temporal con alta precisión.

## Conceptos previos de análisis del Sistema Nervioso Autónomo mediante HRV y Transformada Wavelet
El Sistema Nervioso Autónomo regula funciones vitales como la frecuencia cardíaca, siendo clave en la Variabilidad de la Frecuencia Cardíaca (HRV); el cual es un indicador de salud cardiovascular que  se evidencia en las variaciones en los intervalos del ciclo cardiaco. Un mayor HRV indica un SNA equilibrado, mientras que una reducción puede asociarse a estrés o patologías .

El Sistema Nervioso Autónomo (SNA) regula funciones vitales como la frecuencia cardíaca, desempeñando un papel fundamental en la Variabilidad de la Frecuencia Cardíaca (HRV). Este parámetro, que cuantifica las variaciones en los intervalos del ciclo cardíaco (R-R), constituye un importante indicador de salud cardiovascular. Valores elevados de HRV reflejan un equilibrio adecuado del SNA, mientras que su disminución puede asociarse a condiciones de estrés o diversas patologías cardíacas. Para su análisis, la Transformada Wavelet es una herramienta importante puesto que permite descomponer la señal ECG en diferentes componentes frecuenciales, identificando patrones temporales y espectrales que métodos tradicionales (como la FFT) podrían pasar por alto. Esto facilita la detección de alteraciones en el dominio del tiempo-frecuencia, ofreciendo una visión más completa de la dinámica cardíaca y su relación con el SNA.


![image](https://github.com/user-attachments/assets/25b2aa97-2656-469d-9434-57fb6d3c9407) 





Para el desarrollo de este trabajo se utilizo una wavelwet tipo morlet la cual nos permite descomponer la señal ECG en sus componentes frecuenciales e identificar patrones temporales y espectrales complejos. El componente de baja frecuencia (LF, 0.04-0.15 Hz), que refleja predominantemente la actividad simpática modulada por los barorreflejos, y la banda de alta frecuencia (HF, 0.15-0.4 Hz), asociada a la influencia parasimpática y sincronizada con la respiración. El cociente LF/HF cuantifica el equilibrio autonómico, donde valores elevados sugieren predominio simpático, mientras que valores reducidos indican mayor tono vagal, proporcionando así información clínicamente relevante sobre la regulación cardiovascular.  Sirve para evaluar el equilibrio entre el sistema simpático y parasimpático. 

![image](https://github.com/user-attachments/assets/b8b23c58-225d-49c5-9a56-25c0050524bc)


El RMSSD (Raíz Cuadrada de la Media de las Diferencias Sucesivas) es un indicador de la actividad del sistema nervioso parasimpático, donde valores elevados reflejan un estado de recuperación óptimo de  un tema físico y mental. Por el contrario, un RMSSD reducido sugiere predominio de la actividad simpática, vinculado a situaciones de estrés, fatiga, sobreentrenamiento. Por su parte, el pNN50 (Porcentaje de Intervalos R-R con Diferencias Superiores a 50 ms) cuantifica la variabilidad instantánea entre latidos: un porcentaje alto indica una función autonómica saludable y un estado de relajación, mientras que valores bajos pueden señalar estrés, ansiedad o deterioro en la regulación cardiovascular. Ambos parámetros, en conjunto, proporcionan una visión integral del equilibrio autonómico y su relación con el estado fisiológico y clínico del individuo.

Desviación estándar:
![image](https://github.com/user-attachments/assets/9f63ced9-92a0-43dc-b519-ecf8094b1555)


![image](https://github.com/user-attachments/assets/f5a49a1f-5dec-484b-b6bf-c7b6f47641a2) 

![image](https://github.com/user-attachments/assets/078bef15-bc74-43c2-b8ce-f69f1839af08)


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
Se implementa una función para guardar los datos, con el objetivo de permitir su posterior procesamiento. Esto facilita la eliminación de artefactos, ruido y componentes no deseados, lo que a su vez permite realizar un análisis más detallado de las características fisiológicas relevantes.
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
## Procesamiento

Se toma un filtro tipo IIR (Filtro Digital de Respuesta Infinita al Impulso) el cual en señales electrocardiográficas (ECG) permite eliminar ruidos y artefactos que interfieren con la correcta interpretación de la señal, sin dañar las características importantes del ECG. Este tipo de filtro ayuda a eliminar interferencias de baja frecuencia, como la deriva de línea base causada por movimientos o respiración, y ruidos de alta frecuencia, como interferencias eléctricas y actividad muscular (EMG). Al filtrar estas componentes indeseadas, se mejora la calidad de la señal y se facilita la detección precisa de eventos cardíacos como los complejos QRS, ondas P y T.  Aparte son eficientes a nivel computacionales, permitiendo un procesamiento en tiempo real con un bajo costo computacional. Para el diseño en  nuestro trabajo se toma en los rangos de una frecuencia baja de 0.5  Hz y la frecuencia de 45 Hz. 

```pyton
 def init_filter(self):
        fc_baja = 0.5
        fc_alta = 45
        fn_baja = fc_baja / (0.5 * self.fm)
        fn_alta = fc_alta / (0.5 * self.fm)
        orden = 2
        self.b, self.a = butter(orden, [fn_baja, fn_alta], btype='band')
```
A continuación, se mostrará la forma en que se crea la wavelet para la señal, así como las gráficas utilizadas para el análisis de las frecuencias.
```pyton
import pywt

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
```

#### Usuario normal
![image](https://github.com/user-attachments/assets/5d32a850-1300-4204-a5ff-55726ff5bc90)

![image](https://github.com/user-attachments/assets/e876e39f-5d11-4b48-8334-32395e3d4959)


![image](https://github.com/user-attachments/assets/cda3b57d-9da1-40e9-86c4-f203a9e6e13c)


 Se toma un espectrograma por medio de la wavelet, en este caso Morlet. Gracias a esto, podemos analizar la potencia de nuestra señal. Además, se generan gráficas para el análisis que se realizará después con el usuario estresado.
#### Usuario en estado de estres

![image](https://github.com/user-attachments/assets/af82bf13-b33e-43a4-b7da-4be94bbfdda9)

![image](https://github.com/user-attachments/assets/49598465-e4df-4863-a080-e1e84953eecc)


![image](https://github.com/user-attachments/assets/20eca59d-8610-434e-a3bc-d1f5d4cb8b4b)



El RMSSD, así como el pNN50, son más altos en el usuario normal. Esto quiere decir que sí hay influencia del sistema simpático y que realmente esta variación muestra cómo cambia el estado de nuestro paciente, aunque no se llega al objetivo, que era un porcentaje más bajo.

Como podemos evidenciar, se revisan las frecuencias y, en comparación, se logran observar algunos cambios clave. Entre estos, se nota que hay un poco más de inestabilidad en las curvas del usuario en estrés, así como también una mayor intensidad en algunas zonas rojas, lo cual indica que la onda tiene mayor energía. Esto se debe a una mayor actividad simpática. Aparte tambien podemos evidenciar que las rojas actuan alrededor del complejo QRS y las azules  despues lo que representa la ST.
![image](https://github.com/user-attachments/assets/97bf5d14-2d90-42a5-bb9f-126f07d59f9f)

La importancia de esta  radica en el poder analizar variaciones en la actividad autónoma del corazón (HRV).  La escala utilizada es en términos de frecuencia, específicamente de 0 a 0.5 Hz, porque eso es lo que corresponde a los rangos fisiológicos típicos de la variabilidad cardíaca (HRV).



## Anexo: Diagrama de flujo y preprocesamiento de la señal


Se elaboro un diagrama  donde podrmos conocer el expliciatamente cómo llevarán a cabo el proyecto, las técnicas y herramientas que van a utilizar y los resultados que vana obtener
Anexo 

Describe completamente el diseño de los filtros utilizados con todos sus parámetros, y justifica adecuadamente su elección.
