# Laboratorio 5 - Heart Rate Variation
## Introducción
En esta práctica se analizó la variabilidad de la frecuencia cardíaca (HRV) a partir de una señal ECG utilizando Python y librerías como NumPy, SciPy, Matplotlib y PyWavelets. El proceso incluyó filtrado digital, detección de picos R, cálculo de intervalos R-R y análisis en el dominio del tiempo y tiempo-frecuencia mediante la transformada Wavelet, la cual permite identificar cómo varían las frecuencias a lo largo del tiempo con alta resolución temporal. Estos cambios reflejan la actividad del sistema nervioso autónomo: la frecuencia cardíaca aumenta por predominio simpático y disminuye por influencia parasimpática ,  para estimular las dos partes se realizo una investigación para la cual se determinó que el ejercicio y esfuerzo fisico aumenta la frecuencia cardiaca por lo que al inicio de la señal la frecuencia cardiaca es mayor con respecto al final donde esta fue disminuyendo hasta estabilizarse. 
## Requerimientos:

-Interfaz de python (para este caso 3.12)
-Numpy
-matplotlib.pyplot
-scip-y.signal  butter, filtfilt, find_peaks
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
```

```bash 

```
