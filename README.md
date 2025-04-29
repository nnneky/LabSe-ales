# Laboratorio 5 - Heart Rate Variation
## Introducción
En esta práctica se analizó la variabilidad de la frecuencia cardíaca (HRV) a partir de una señal ECG utilizando Python y librerías como NumPy, SciPy, Matplotlib y PyWavelets. El proceso incluyó el filtrado digital de la señal para eliminar artefactos, seguido de la detección de picos R y el cálculo de los intervalos R-R, fundamentales para el análisis de HRV. Se realizaron análisis en el dominio del tiempo, y en el dominio tiempo-frecuencia utilizando la transformada Wavelet, que permite observar cómo varían las frecuencias a lo largo del tiempo con alta resolución temporal. Estos cambios reflejan la influencia del sistema nervioso autónomo: el predominio simpático acelera la frecuencia cardíaca, mientras que la actividad parasimpática la reduce. El análisis obtenido permitió demostrar que el HRV es una herramienta sensible y efectiva para evaluar el estado fisiológico del sistema cardiovascular.
## Requerimientos:

-Interfaz de python (para este caso 3.12)

-Numpy

-matplotlib.pyplot

-scipy.signal 

-pywt

## FUNDAMENTOS TEÓRICOS:

### Actividad simpática y parasimpática del sistema nervioso autónomo
Regula de forma complementaria diversas funciones fisiológicas, incluida la frecuencia cardíaca. La actividad simpática tiende a aumentar la frecuencia cardíaca al preparar al cuerpo para situaciones de alerta, mientras que la actividad parasimpática la disminuye, promoviendo el descanso y la recuperación.

### Variabilidad de la frecuencia cardiaca (HRV) 
La variabilidad de la frecuencia cardíaca (HRV) se refiere a las fluctuaciones en el intervalo R-R (es decir, el tiempo entre dos picos sucesivos R en el ECG), lo que refleja el control autonómico del corazón. Esta variabilidad es un indicador sensible del equilibrio entre la actividad simpática y parasimpática del sistema nervioso autónomo.

En el análisis espectral de la HRV, las fluctuaciones se descomponen en diferentes bandas de frecuencia, cada una asociada a distintos mecanismos fisiológicos. Las frecuencias de interés más comunes en este análisis son:

- VLF (Very Low Frequency): 0.003 – 0.04 Hz.

- LF (Low Frequency): 0.04 – 0.15 Hz (Se asocia con una combinación de actividad simpática y parasimpática)

- HF (High Frequency): 0.15 – 0.4 Hz (Se relaciona principalmente con la actividad parasimpática (vagal), especialmente con la respiración (arritmia sinusal respiratoria))

### Transformada Wavelet
La transformada wavelet (WT) descompone una señal en versiones escaladas y desplazadas de una función base llamada wavelet madre. Esta función tiene características localizadas tanto en el tiempo como en la frecuencia, lo que permite el análisis multi-resolución.

### Usos principales en señales biológicas

- Detección de eventos transitorios (ej. complejos QRS en ECG).

- Descomposición multi-resolución para analizar componentes de alta y baja frecuencia.

- Eliminación de ruido y artefactos.

- Análisis espectro-temporal.

- Compresión de datos sin perder información relevante.

### Tipos de wavelets comunes

Daubechies: Buena para compactación y ortogonalidad.

Symlets: Más simétricas, útiles en análisis de señales biológicas.

Coiflets: Con más momentos nulos, útiles en EEG y EMG.

Haar: Simple y rápida, usada para segmentación o compresión.

Morlet: Usada en CWT para análisis tiempo-frecuencia.

Mexican Hat (Ricker): Adecuada para detectar eventos rápidos.

## Explicación Código: 
Librerías utilizadas: 
```bash 
import numpy as np  # librería para trabajar con arrays
import matplotlib.pyplot as plt # Librería para graficar
from scipy.signal import butter, filtfilt, find_peaks # butter creafiltros butterworth, filtfilt alpica el filtro en 2 direccopnes y find peaks detecta picos en la señal
import pywt # Librería para transformada Wavelet
```

Cargar la señal ECG:

```bash 
fs = 1000  # frecuencia de muestreo 
ecg_signal = np.loadtxt('SARA02.txt')  # carga la señal desde un archivo de texto
t = np.arange(len(ecg_signal)) / fs    # vector de tiempo asociado a la señal
```
Se crea un filtro pasa banda: 

```bash 
def butter_bandpass(lowcut, highcut, fs, order=4): #  diseña un filtro Butterworth pasa banda de cuarto orden 
    nyq = 0.5 * fs # Se calcula la frecuencia de Nyquist
    low = lowcut / nyq  
    high = highcut / nyq # Se normalizan las frecuencias 
    b, a = butter(order, [low, high], btype='band')   # Se  calcula los coeficientes del filtro
    return b, a
def apply_filter(data, lowcut, highcut, fs, order=4): # Llama a butter_bandpass para crear el filtro.
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)  # aplica el filtro de forma acausal (sin desfase) # Aplica el filtro usando filtfilt que filtra hacia adelante y hacia atrás para poder eliminar el desfase
    return y
filtered_ecg = apply_filter(ecg_signal, 0.5, 40.0, fs) # Se filtra la señal para dejar solo frecuencias entre 0.5 Hz y 40 Hz, que son las relevantes en ECG.
```
Se grafica la señal filtrada: 
```bash 
plt.figure(figsize=(15, 4))
plt.plot(t, filtered_ecg)
plt.title('Señal ECG filtrada')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()
plt.show()
```
Detección de picos R:

```bash
peaks, properties = find_peaks(filtered_ecg, distance=0.6*fs, height=np.std(filtered_ecg)) #los picos deben estar separados al menos 0.6 segundos donde find_peaks detecta picos locales en la señal y height=np.std(filtered_ecg) hacen que detecte solo picos con una altura mayor al valor típico
rpeak_times = peaks / fs #tiempo de cada pico en segundos. 
rr_intervals = np.diff(rpeak_times) * 1000  # en milisegundos
# Se grafica la señal filtrada con los picos R marcados como puntos rojos ('rx')
plt.figure(figsize=(15, 4))
plt.plot(t, filtered_ecg)
plt.plot(peaks/fs, filtered_ecg[peaks], "rx")
plt.title('Detección de Picos R')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()
plt.show()    
```
