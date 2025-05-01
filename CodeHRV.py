import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, find_peaks
import pywt
from scipy.interpolate import interp1d

# --------------------------------------
# 1. Cargar señal ECG y convertir a mV
# --------------------------------------
fs = 400  # Hz
raw_ecg = np.loadtxt('PAULA02.txt')

# Conversión de unidades ADC a milivoltios (1 mV ≈ 200 unidades)
mV_per_unit = 1 / 120
ecg_signal = (raw_ecg - np.mean(raw_ecg)) * mV_per_unit  # ahora está en mV

t = np.arange(len(ecg_signal)) / fs

plt.figure(figsize=(15, 4))
plt.plot(t, ecg_signal)
plt.title('Señal ECG original')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (mV)')
plt.grid()
plt.show()

# --------------------------------------
# 2. Diseñar filtro IIR Butterworth
# --------------------------------------
def bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    
    # Mostrar los coeficientes b y a (Ecuación en diferencias)
    print(f"Ecuación en diferencias del filtro IIR (coeficientes b, a):\n")
    print("Coeficientes b (numerador):", b)
    print("Coeficientes a (denominador):", a)
    
    return b, a

# --------------------------------------
# 3. Aplicar filtro con lfilter
# --------------------------------------
b, a = bandpass(0.1, 50, fs, order=4)

# Aplicar filtro IIR usando lfilter (automáticamente con condiciones iniciales en 0)
filtered_ecg = lfilter(b, a, ecg_signal)

# Graficar ECG filtrado
plt.figure(figsize=(15, 4))
plt.plot(t, filtered_ecg)
plt.title('Señal ECG filtrada con filtro IIR (usando lfilter)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (mV)')
plt.grid()
plt.show()

# --------------------------------------
# 4. Detección de Picos R
# --------------------------------------
peaks, _ = find_peaks(filtered_ecg, distance=0.6*fs, height=np.std(filtered_ecg))
rpeak_times = peaks / fs
rr_intervals = np.diff(rpeak_times) * 1000  # ms

# Graficar picos R
plt.figure(figsize=(15, 4))
plt.plot(t, filtered_ecg)
plt.plot(peaks / fs, filtered_ecg[peaks], "rx")
plt.title('Detección de Picos R')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (mV)')
plt.grid()
plt.show()

# --------------------------------------
# 5. Análisis en el dominio del tiempo
# --------------------------------------
mean_rr = np.mean(rr_intervals)
std_rr = np.std(rr_intervals)

print(f"Media RR: {mean_rr:.2f} ms")
print(f"Desviación estándar RR: {std_rr:.2f} ms")

plt.figure(figsize=(12, 4))
plt.plot(rr_intervals, marker='o')
plt.axhline(mean_rr, color='red', linestyle='--', label='Media RR')
plt.title('Intervalos RR')
plt.xlabel('Latido')
plt.ylabel('Intervalo RR (ms)')
plt.legend()
plt.grid()
plt.show()

# --------------------------------------
# 6. Señal de HRV interpolada
# --------------------------------------
rr_times = rpeak_times[1:]  # timestamps de los intervalos RR
interp_fs = 4  # Hz recomendado para HRV
new_time = np.arange(rr_times[0], rr_times[-1], 1/interp_fs)
rr_interpolated = interp1d(rr_times, rr_intervals, kind='cubic')(new_time)

# --------------------------------------
# 7. Análisis en frecuencia con Wavelet
# --------------------------------------
wavelet = 'morl'
scales = np.arange(1, 128)
coefficients, frequencies = pywt.cwt(rr_interpolated, scales, wavelet, 1/interp_fs)

# Limitar a frecuencias fisiológicas relevantes (0-0.5 Hz)
freq_limit = 0.5
mask = frequencies <= freq_limit
coefficients = coefficients[mask]
frequencies = frequencies[mask]

plt.figure(figsize=(12, 6))
plt.imshow(np.abs(coefficients), extent=[0, len(rr_interpolated)/interp_fs, frequencies[-1], frequencies[0]],
           cmap='jet', aspect='auto')
plt.title('Espectrograma HRV (Wavelet)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia (Hz)')
plt.colorbar(label='Potencia')
plt.show()