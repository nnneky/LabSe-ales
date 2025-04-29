# Laboratorio 5 - Heart Rate Variation
## Introducción
En esta práctica se analizó la variabilidad de la frecuencia cardíaca (HRV) a partir de una señal ECG utilizando Python y librerías como NumPy, SciPy, Matplotlib y PyWavelets. El proceso incluyó el filtrado digital de la señal para eliminar artefactos, seguido de la detección de picos R y el cálculo de los intervalos R-R, fundamentales para el análisis de HRV. Se realizaron análisis en el dominio del tiempo, y en el dominio tiempo-frecuencia utilizando la transformada Wavelet, que permite observar cómo varían las frecuencias a lo largo del tiempo con alta resolución temporal. Estos cambios reflejan la influencia del sistema nervioso autónomo: el predominio simpático acelera la frecuencia cardíaca, mientras que la actividad parasimpática la reduce. El análisis obtenido permitió demostrar que el HRV es una herramienta sensible y efectiva para evaluar el estado fisiológico del sistema cardiovascular.
## Requerimientos:

-Interfaz de python (para este caso 3.12)

-Numpy

-matplotlib.pyplot

-scipy.signal 

-pywt

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
