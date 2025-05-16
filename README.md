# LAB-5- Variabilidad de la Frecuencia Cardiaca usando la Transformada Wavelet
## Introducción 
En esta práctica de laboratorio se realizó la captura de una señal electrocardiográfica (ECG) y su posterior preprocesamiento, con el objetivo de analizar en profundidad las características de la actividad cardíaca. Un aspecto fundamental del estudio fue el análisis de la variabilidad de la frecuencia cardíaca (HRV), un parámetro clave para evaluar el funcionamiento del sistema nervioso autónomo y la salud cardiovascular en general. Para ello, se empleó la transformada wavelet, una herramienta matemática que permite identificar cambios en las frecuencias características de la señal y analizar su dinámica temporal con alta precisión.

## Conceptos previos de análisis del Sistema Nervioso Autónomo mediante HRV y Transformada Wavelet
El Sistema Nervioso Autónomo (SNA) regula funciones fisiológicas esenciales, entre ellas la frecuencia cardíaca, y desempeña un papel crucial en la modulación de la Variabilidad de la Frecuencia Cardíaca (HRV, por sus siglas en inglés). Este parámetro, que cuantifica las fluctuaciones en los intervalos entre latidos consecutivos (intervalos R-R), se considera un indicador sensible del estado funcional del SNA y de la salud cardiovascular en general. Valores elevados de HRV suelen estar asociados a un adecuado equilibrio entre las ramas simpática y parasimpática del SNA, reflejando una buena capacidad de adaptación fisiológica ante estímulos externos. En contraste, una reducción en la HRV puede estar relacionada con estados de estrés, disfunción autonómica o la presencia de patologías cardiovasculares.

Para el análisis de la HRV, la Transformada Wavelet representa una herramienta analítica robusta, ya que permite la descomposición multiescala de la señal ECG en distintos componentes frecuenciales. A diferencia de métodos clásicos como la Transformada Rápida de Fourier (FFT), la wavelet ofrece una resolución simultánea en tiempo y frecuencia, lo cual es especialmente útil para estudiar señales no estacionarias como el ECG. Esta capacidad permite identificar con mayor precisión eventos transitorios, modulaciones de frecuencia y patrones de comportamiento autonómico, proporcionando así una caracterización más detallada de la dinámica cardíaca.


![image](https://github.com/user-attachments/assets/25b2aa97-2656-469d-9434-57fb6d3c9407) 

Para el desarrollo de este trabajo se utilizó una wavelet tipo Morlet, la cual permite descomponer la señal ECG en sus componentes frecuenciales e identificar patrones temporales y espectrales complejos con alta resolución. Esta transformada resulta particularmente útil para el análisis de la Variabilidad de la Frecuencia Cardíaca (HRV), ya que facilita la evaluación simultánea en el dominio tiempo-frecuencia. Entre los componentes de interés se encuentran la banda de baja frecuencia (LF, 0.04–0.15 Hz), que refleja predominantemente la actividad simpática modulada por los barorreflejos, y la banda de alta frecuencia (HF, 0.15–0.4 Hz), estrechamente relacionada con la actividad parasimpática y sincronizada con el ritmo respiratorio. El cociente entre ambas (LF/HF) se utiliza comúnmente como un índice del equilibrio autonómico: valores elevados indican un predominio simpático, mientras que valores bajos sugieren una mayor influencia vagal. Esta relación proporciona información clínicamente relevante sobre la modulación cardiovascular por parte del sistema nervioso autónomo, permitiendo una evaluación más precisa del estado fisiológico del individuo.

![image](https://github.com/user-attachments/assets/b8b23c58-225d-49c5-9a56-25c0050524bc)

El RMSSD (Root Mean Square of the Successive Differences) es un parámetro en el dominio del tiempo que refleja la actividad del sistema nervioso parasimpático. Valores elevados de RMSSD se asocian con un estado fisiológico de recuperación eficiente y equilibrio autonómico, tanto a nivel físico como mental. En contraste, valores reducidos indican un predominio simpático, lo cual puede estar vinculado a estados de estrés agudo, fatiga o sobreentrenamiento. Por su parte, el pNN50 (porcentaje de intervalos R-R consecutivos que difieren en más de 50 ms) cuantifica la variabilidad a corto plazo de la frecuencia cardíaca. Un porcentaje elevado de pNN50 se asocia con una mayor modulación parasimpática y un estado de relajación, mientras que valores bajos pueden reflejar disfunción autonómica, estrés crónico o trastornos cardiovasculares. En conjunto, ambos indicadores ofrecen una evaluación complementaria y robusta del tono autonómico y su impacto sobre el estado fisiológico y clínico del individuo.

**Desviación estándar:**

![image](https://github.com/user-attachments/assets/9f63ced9-92a0-43dc-b519-ecf8094b1555)

![image](https://github.com/user-attachments/assets/f5a49a1f-5dec-484b-b6bf-c7b6f47641a2) 

![image](https://github.com/user-attachments/assets/078bef15-bc74-43c2-b8ce-f69f1839af08)

## Características de la señal adquirida
Para la adquisición de la señal electrocardiográfica (ECG), se empleó una tarjeta de adquisición de datos NI DAQ-6004, la cual proporciona una resolución de 12 bits, correspondiente a 4096 niveles de cuantización. La frecuencia de muestreo se configuró en 800 Hz, un valor considerablemente superior al mínimo establecido por el teorema de Nyquist. Dado que las componentes espectrales de la señal ECG se encuentran típicamente en el rango de 0.05 Hz a 100 Hz, una frecuencia de muestreo de al menos 200 Hz sería teóricamente suficiente para evitar aliasing. No obstante, se optó por una frecuencia más elevada con el fin de capturar con mayor precisión los detalles transitorios y mejorar la calidad general de la señal adquirida. Esta configuración implica un intervalo de muestreo de 1.25 milisegundos entre cada muestra.

En esta primera etapa del experimento, se realizó la captura de la señal ECG en condiciones de reposo, registrando las variaciones de voltaje asociadas a la actividad eléctrica del corazón. La señal obtenida corresponde a una versión cruda o sin procesar, en la cual pueden observarse picos anómalos y presencia de ruido, lo que evidencia la necesidad de un adecuado preprocesamiento para su análisis posterior.

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
Se implementó una función para el almacenamiento de los datos adquiridos, con el objetivo de facilitar su posterior procesamiento. Esta etapa resulta fundamental, ya que permite aplicar técnicas de filtrado y eliminación de artefactos, reduciendo el ruido y suprimiendo componentes no deseados presentes en la señal cruda. De este modo, se mejora significativamente la calidad de la señal, lo cual es esencial para llevar a cabo un análisis preciso y detallado de las características fisiológicas relevantes contenidas en la señal electrocardiográfica.

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
Se utilizó un filtro digital de tipo IIR (Infinite Impulse Response), el cual resulta especialmente adecuado para el procesamiento de señales electrocardiográficas (ECG), ya que permite eliminar ruidos y artefactos sin afectar las características fisiológicas esenciales de la señal. Este tipo de filtro es eficaz para suprimir interferencias de baja frecuencia, como la deriva de la línea base provocada por movimientos del paciente o el ciclo respiratorio, así como ruidos de alta frecuencia asociados a interferencias eléctricas o actividad muscular (EMG).

La aplicación de este filtrado mejora significativamente la relación señal-ruido, facilitando la identificación precisa de eventos cardíacos clave, como los complejos QRS, y las ondas P y T. Además, los filtros IIR presentan ventajas computacionales al requerir menos recursos que otros tipos de filtros, como los FIR, lo que los hace adecuados para implementaciones en tiempo real y sistemas embebidos.

En el presente trabajo, el filtro fue diseñado para conservar el contenido espectral relevante de la señal ECG, estableciendo un rango de paso de banda entre 0.5 Hz y 45 Hz. Este rango permite preservar las componentes fundamentales de la señal cardíaca mientras se atenúan las frecuencias no deseadas, garantizando así una mejor calidad para el análisis posterior.

![image](https://github.com/user-attachments/assets/aed0cf61-3d7a-45e1-a5c9-45dbaff8d32f) 

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

Se utilizó un espectrograma obtenido mediante la Transformada Wavelet Continua (CWT), empleando en este caso una wavelet tipo Morlet. Esta herramienta permite representar la distribución de la potencia de la señal ECG en el dominio tiempo-frecuencia, proporcionando una visualización detallada de los cambios dinámicos en las componentes frecuenciales a lo largo del tiempo. Esta representación resulta especialmente útil para identificar patrones transitorios y variaciones en la actividad autonómica que podrían no ser evidentes mediante técnicas espectrales tradicionales.

Adicionalmente, se generaron gráficas que servirán como referencia para el análisis comparativo en una fase posterior del experimento, en la cual se evaluará la señal de un usuario sometido a una condición de estrés. Este enfoque permite observar de manera precisa las diferencias en la actividad cardíaca y su modulación autonómica bajo distintos estados fisiológicos.
#### Usuario en estado de estres

![image](https://github.com/user-attachments/assets/af82bf13-b33e-43a4-b7da-4be94bbfdda9)

![image](https://github.com/user-attachments/assets/49598465-e4df-4863-a080-e1e84953eecc)

![image](https://github.com/user-attachments/assets/20eca59d-8610-434e-a3bc-d1f5d4cb8b4b)

Los valores de RMSSD y pNN50 fueron significativamente más altos en el usuario en condición de reposo en comparación con el usuario expuesto a estrés. Estos resultados sugieren una mayor modulación parasimpática en estado basal, lo que es indicativo de un equilibrio autonómico saludable. En contraste, la reducción de estos parámetros en el usuario estresado refleja una activación del sistema simpático, consistente con una respuesta fisiológica al estrés. Si bien la diferencia no alcanzó el objetivo esperado de un descenso marcado en los valores, sí se evidencia una tendencia que valida la sensibilidad de estos indicadores ante cambios en el estado fisiológico.

Adicionalmente, el análisis tiempo-frecuencia mediante la Transformada Wavelet permite observar variaciones relevantes en la distribución espectral de la señal ECG. En el caso del usuario estresado, se detecta una mayor inestabilidad en las curvas espectrales, así como un incremento en la intensidad de las zonas de alta energía (representadas en color rojo), especialmente en torno al complejo QRS. Estas zonas reflejan una mayor densidad energética, probablemente asociada a una activación simpática aumentada. Por otro lado, las regiones de menor energía (colores azulados), ubicadas predominantemente después del complejo QRS, coinciden con el segmento ST, el cual parece menos pronunciado en el usuario bajo estrés, lo que puede reflejar alteraciones en la recuperación eléctrica ventricular.

![image](https://github.com/user-attachments/assets/97bf5d14-2d90-42a5-bb9f-126f07d59f9f)

La importancia de esta representación radica en su capacidad para analizar las variaciones en la actividad autonómica del corazón a través de la Variabilidad de la Frecuencia Cardíaca (HRV). La escala empleada en el análisis espectral se expresa en términos de frecuencia, abarcando el rango de 0 a 0.5 Hz, ya que este intervalo corresponde a los rangos fisiológicos típicos en los que se manifiesta la modulación autonómica de la frecuencia cardíaca. Dentro de este rango, se encuentran las bandas de baja frecuencia (LF: 0.04–0.15 Hz) y alta frecuencia (HF: 0.15–0.4 Hz), asociadas principalmente a la actividad simpática y parasimpática, respectivamente. Este enfoque permite una evaluación detallada y no invasiva del equilibrio entre ambos componentes del sistema nervioso autónomo.

## Anexo: Diagrama de flujo y preprocesamiento de la señal
Protocolo Experimental – Captura de la Señal ECG
Con el objetivo de evaluar la variabilidad de la frecuencia cardíaca (HRV) bajo condiciones de reposo y estrés agudo, se implementó un protocolo experimental controlado que permite una caracterización precisa de la dinámica cardíaca mediante análisis en el dominio del tiempo y tiempo-frecuencia.

**Preparación del Sujeto**
El participante fue ubicado en posición sedente, en un ambiente controlado (22 °C, iluminación tenue, mínima estimulación externa). Se utilizaron electrodos de superficie en una derivación única, con limpieza previa de la piel. La señal ECG fue adquirida mediante una tarjeta NI DAQ-6004 (12 bits, 800 Hz) conectada a un sistema desarrollado en Python.

**Estímulo Previo: Ingesta de Bebida Energética**
Treinta minutos antes de la captura, el sujeto consumió una lata de Red Bull (250 mL, 80 mg de cafeína), cuyo efecto esperado era un aumento en la actividad simpática: incremento de la frecuencia cardíaca, reducción de HRV (RMSSD y pNN50), disminución de HF y aumento relativo de LF.

Fases de la Captura ECG
-La señal se registró durante 15 minutos, abarcando tres fases:

-Reposo inicial (0–2 min): Estado basal post-ingesta sin estímulos externos.

-Estrés agudo (2–4 min): Introducción súbita de un estímulo emocional (interacción inesperada con el teléfono personal por parte de un familiar cercano).

-Recuperación (4–15 min): Fase de reposo posterior para evaluar el retorno progresivo del tono parasimpático.

**Segmentación para Análisis**
Para el análisis, se extrajo una ventana representativa de 5 minutos que incluyó las tres fases clave. Esta segmentación, basada en marcas temporales internas, permitió aplicar métricas de HRV tanto en el dominio del tiempo como en el tiempo-frecuencia mediante la transformada wavelet.

![57b5a679-ba6c-4547-bc09-ceefaab09f78](https://github.com/user-attachments/assets/d6a1d522-8876-4a35-b18b-4dd4fb2f6107)

![57b5a679-ba6c-4547-bc09-ceefaab09f78](https://github.com/user-attachments/assets/b63cf875-1baf-4332-abe3-c0244e9e7ddb)

![6ee3fa31-44c7-47dc-9ee0-7766e5ba66d7](https://github.com/user-attachments/assets/30cedb02-eb3c-4f2f-aa9a-c2e5bf606974)

## Requisistos 
- Python 3.9
- matplotlib
- PyQt5
- matplotlib
- numpy
- scipy
- pywt
- pyserial	
- threading, struct, time	Módulos estándar 

### Contact information
-  est.nikoll.bonilla@unimilitar.edu.co
-  est.hugo.perez@unimilitar.edu.co
-  est.yonatan.franco@unimilitar.edu.co
