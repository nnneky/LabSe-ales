# Laboratorio 5 - Heart Rate Variation
## INTRODUCCIÓN
En esta práctica se analizó la variabilidad de la frecuencia cardíaca (HRV) a partir de una señal ECG utilizando Python y librerías como NumPy, SciPy, Matplotlib y PyWavelets. El proceso incluyó el filtrado digital de la señal para eliminar artefactos, seguido de la detección de picos R y el cálculo de los intervalos R-R, fundamentales para el análisis de HRV. Se realizaron análisis en el dominio del tiempo, y en el dominio tiempo-frecuencia utilizando la transformada Wavelet, que permite observar cómo varían las frecuencias a lo largo del tiempo con alta resolución temporal. Estos cambios reflejan la influencia del sistema nervioso autónomo: el predominio simpático acelera la frecuencia cardíaca, mientras que la actividad parasimpática la reduce. El análisis obtenido permitió demostrar que el HRV es una herramienta sensible y efectiva para evaluar el estado fisiológico del sistema cardiovascular.
## REQUERIMIENTOS

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

### Wavelets usadas en ECG

- #### Daubechies (db4, db6)
son herramientas eficientes para analizar señales biológicas, como el ECG. La db4 tiene 4 coeficientes y es ideal para detección de picos R y análisis de variabilidad de la frecuencia cardíaca (HRV), gracias a su alta resolución temporal. Por otro lado, la db6 con 6 coeficientes ofrece mejor resolución en frecuencia, siendo útil para un análisis más detallado de las frecuencias, aunque con una resolución temporal ligeramente menor. Ambas se utilizan en el procesamiento de señales ruidosas y en la mejora de la precisión del análisis de ECG.

- #### Symlet (Sym2, Sym4)
on variantes de las wavelets de Daubechies diseñadas para ofrecer mayor simetría en su forma, lo que mejora la reconstrucción de señales. La Sym2 tiene 2 coeficientes y es útil para análisis de alta resolución temporal, mientras que la Sym4 con 4 coeficientes ofrece un mejor balance entre resolución temporal y frecuencia. Son ideales para filtrar artefactos y mejorar el análisis de señales biológicas como el ECG y EEG, manteniendo detalles importantes mientras eliminan ruido.

## DISEÑO DEL EXPERIMENTO A IMPLEMENTAR
Con la finalidad de realizar un análisis del HRV, se diseño un experimento de aproximadamente 5 minutos que estimulará la actividad simpática, en dondela frecuencia cárdiaca aumentará y el HRV disminuirá. Para esto se planteo el siguiente diagrama de flujo, el cual describe paso a paso como se ejecutará mencionado experimento

## ADQUSICIÓN DE LA SEÑAL ECG
Para este apartado de la práctica se utilizo un módulo de ecg AD8232, se implemento la siguiente dispocisión de los electrodos, esta ubicación proporciona la derivación II de la señal electrocradiográfica.

![image](https://github.com/user-attachments/assets/ea68d9d7-7353-4c24-bf64-0aeb80847941)

Despues de colocar de forma correcta los electrodos, la salida de datos del sensor se conecto a la stm32 nucleo 411, estos datos serán recividos mediante un ADC y enviados a matlab mediante un protocolo usart, luego en la interfaz del programa se realizará el guardado y tratamiento de la señal en un archivo .txt, Como se muestra a continuación

```bash
function registrar_ecg_5min_completo
    % ECG 5 minutos con visualización en vivo y guardado a archivo

    % Limpia la consola, las variables del workspace y cierra figuras
    clc; clear; close all;

    %% Configuración del puerto serie
    puerto  = 'COM3';         % Nombre del puerto COM utilizado
    baudios = 115200;         % Velocidad de transmisión (baudios)

    try
        % Crea un objeto de puerto serie con los parámetros dados
        sp = serialport(puerto, baudios);
        % Configura el terminador de línea como salto de línea (LF, hace que pase a la siguiente linea luego de imprimir texto)
        configureTerminator(sp, "LF");
        % Tiempo máximo de espera para una lectura
        sp.Timeout = 1;
        % Limpia cualquier dato residual en el buffer del puerto serie
        flush(sp);
    catch
        % Si no se puede abrir el puerto, muestra error
        error('No se pudo abrir el puerto %s. Verifique conexión.', puerto);
    end

    %% Archivo de registro
    nombreArchivo = 'ECG_1.txt'; % Nombre del archivo donde se guarda la señal
    fid = fopen(nombreArchivo, 'w'); % Abre archivo para escritura
    if fid == -1
        % Si no se puede abrir el archivo, cierra puerto y muestra error
        clear sp;
        error('No se pudo crear el archivo %s.', nombreArchivo);
    end

    %% Parámetros de adquisición
    T_total      = 300;    % Tiempo total de adquisición (en segundos)
    plotInterval = 0.1;    % Intervalo de actualización del gráfico (s)
    ventanaMM    = 5;      % Tamaño de ventana para media móvil (suavizado)
    bufSize      = 500;    % Cantidad de muestras a mostrar en el gráfico

    % Inicialización de buffers para la señal cruda y filtrada
    datos   = zeros(1, bufSize, 'uint8');   % Buffer crudo (sin filtrar)
    datosF  = zeros(1, bufSize);            % Buffer filtrado (media móvil)

    % Inicializa temporizadores para controlar duración total y gráficos
    tStart  = tic;           % Tiempo de inicio de adquisición
    lastPlot = tic;          % Tiempo del último gráfico actualizado

    %% Preparar figura
    % Crea una figura nueva con título personalizado
    hFig  = figure('Name','ECG 5 min','NumberTitle','off');
    % Traza la señal cruda en azul
    hRaw  = plot(datos, 'b', 'LineWidth', 1); hold on;
    % Traza la señal filtrada en rojo
    hFilt = plot(datosF,'r', 'LineWidth', 1);
    % Escala del eje Y (valores entre 0 y 255 para uint8)
    ylim([0, 255]); grid on;
    % Etiquetas de los ejes
    xlabel('Muestras'); ylabel('Valor (uint8)');
    % Título con el tiempo transcurrido
    hTitle = title('0 / 300 s','FontSize',12);

    %% Bucle principal de captura
    while toc(tStart) < T_total
        % Si hay datos disponibles en el puerto serie
        if sp.NumBytesAvailable > 0
            % Leer todos los datos disponibles como uint8
            muestras = read(sp, sp.NumBytesAvailable, 'uint8');
            % Guardar cada muestra en el archivo de texto
            fprintf(fid, '%u\n', muestras);

            % Actualizar buffer de señal cruda desplazando y agregando nuevas muestras
            datos = [datos(length(muestras)+1:end), muestras];
            % Aplicar media móvil para suavizar la señal
            datosF = movmean(datos, ventanaMM);
        end

        % Actualizar gráfica si ha pasado suficiente tiempo
        if toc(lastPlot) > plotInterval
            % Actualiza los datos del gráfico
            set(hRaw,  'YData', datos);
            set(hFilt, 'YData', datosF);
            % Actualiza el título con el tiempo transcurrido
            set(hTitle,'String', sprintf('%.1f / 300 s', toc(tStart)));
            % Redibuja figura de forma eficiente
            drawnow limitrate;
            % Reinicia temporizador para el siguiente gráfico
            lastPlot = tic;
        end
    end

    %% Finalización
    fclose(fid);     % Cierra el archivo de texto
    clear sp;        % Libera el puerto serie
    fprintf('→ Captura finalizada. Datos guardados en %s\n', nombreArchivo); % Mensaje final
end


```
## PRE-PROCESAMIENTO DE LA SEÑAL ECG




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
