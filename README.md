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

### Wavelets más usadas en ECG

- #### Daubechies (db4, db6)
son herramientas eficientes para analizar señales biológicas, como el ECG. La db4 tiene 4 coeficientes y es ideal para detección de picos R y análisis de variabilidad de la frecuencia cardíaca (HRV), gracias a su alta resolución temporal. Por otro lado, la db6 con 6 coeficientes ofrece mejor resolución en frecuencia, siendo útil para un análisis más detallado de las frecuencias, aunque con una resolución temporal ligeramente menor. Ambas se utilizan en el procesamiento de señales ruidosas y en la mejora de la precisión del análisis de ECG.

- #### Symlet (Sym2, Sym4)
on variantes de las wavelets de Daubechies diseñadas para ofrecer mayor simetría en su forma, lo que mejora la reconstrucción de señales. La Sym2 tiene 2 coeficientes y es útil para análisis de alta resolución temporal, mientras que la Sym4 con 4 coeficientes ofrece un mejor balance entre resolución temporal y frecuencia. Son ideales para filtrar artefactos y mejorar el análisis de señales biológicas como el ECG y EEG, manteniendo detalles importantes mientras eliminan ruido.

- #### Morlet
La transformada wavelet Morlet es ideal para el análisis de señales ECG y la medición de la HRV porque permite una resolución tanto en el tiempo como en la frecuencia, adaptándose a las características dinámicas de las señales. Esto facilita la detección precisa de eventos cardíacos y la identificación de las fluctuaciones de la frecuencia cardíaca en diferentes bandas, esenciales para evaluar la variabilidad cardíaca y el equilibrio del sistema nervioso autónomo.

## DISEÑO DEL EXPERIMENTO A IMPLEMENTAR
Con la finalidad de realizar un análisis del HRV, se diseño un experimento de aproximadamente 5 minutos que estimulará la actividad simpática, en dondela frecuencia cárdiaca aumentará y el HRV disminuirá. Para esto se planteo el siguiente diagrama de flujo, el cual describe paso a paso como se ejecutará mencionado experimento

## ADQUSICIÓN DE LA SEÑAL ECG
Para este apartado de la práctica se utilizo un módulo de ecg AD8232, se implemento la siguiente dispocisión de los electrodos, esta ubicación proporciona la derivación II de la señal electrocradiográfica.

![image](https://github.com/user-attachments/assets/ea68d9d7-7353-4c24-bf64-0aeb80847941)

Despues de colocar de forma correcta los electrodos, la salida de datos del sensor se conecto a la stm32 nucleo 411, estos datos serán recividos mediante un ADC (con una frecuencia de muestreo de 400 Hz) y enviados a matlab mediante un protocolo usart, luego en la interfaz del programa se realizará el guardado y tratamiento de la señal en un archivo .txt, Como se muestra a continuación

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
Luego de ejecutar lo anterior, se obtuvo la siguiente señal

![image](https://github.com/user-attachments/assets/8d804c0a-e0e0-47fc-99fd-2d733e38d91a)


## PRE-PROCESAMIENTO DE LA SEÑAL ECG
Despues de obtener la señal ecg bajo las condiciones optimas, se realizó una preparación de la señal, antes de implementar la transformada wavelt, este proceso previo incluyó:

#### Importación de la señal y librerias a implementar

```bash
import numpy as np ## Cálculos numéricos eficientes en arreglos y matrices.
import matplotlib.pyplot as plt ## Permite graficar señales, espectros, resultados del procesamiento
from scipy.signal import butter, lfilter, find_peaks ## Procesamiento de señales.
import pywt ## Transformada Wavelet Discreta (DWT).
from scipy.interpolate import interp1d

# --------------------------------------
# 1. Cargar señal ECG
# --------------------------------------
fs = 400  # frecuencia de muestreo en Hz
ecg_signal = np.loadtxt('ecg01.txt') ## importar señal ecg del archivo .txt
t = np.arange(len(ecg_signal)) / fs ##  Crea el vector de tiempo (t) correspondiente a cada muestra del ECG


```

#### filtro IIR de acuerdo con los parámetros de la señal y Ecuación en diferencias del filtro

```bash

def bandpass(lowcut, highcut, fs, order=4): ## Define la función bandpass con los siguientes parámetros:lowcut: frecuencia de corte inferior (Hz),highcut: frecuencia de corte superior (Hz),fs: frecuencia de muestreo (Hz),order: orden del filtro (por defecto 4).
    nyq = 0.5 * fs ## frecuencia de nyquist (normalizar frecuencias)
    low = lowcut / nyq ## Normaliza la frecuencia de corte lowcut respecto a Nyquist, ya que la función butter espera frecuencias entre 0 y 1.
    high = highcut / nyq ## Normaliza la frecuencia de corte highcut respecto a Nyquist, ya que la función butter espera frecuencias entre 0 y 1.
    b, a = butter(order, [low, high], btype='band')  ## Diseña un filtro Butterworth pasa banda de orden dado, b: coeficientes del numerador (parte directa de la ecuación), a: coeficientes del denominador (parte recursiva).
    
    # Mostrar los coeficientes b y a (Ecuación en diferencias) 
    print(f"Ecuación en diferencias del filtro IIR (coeficientes b, a):\n")
    print("Coeficientes b (numerador):", b)
    print("Coeficientes a (denominador):", a)


b, a = bandpass(0.1, 50, fs, order=4) ## define un filtro pasa bandas con frecuencias pasantes desde 0.5 a 50 Hz, de orden 4 en donde b son los coeficientes del denominador y a del denominador 

# Aplicar filtro IIR usando lfilter (automáticamente con condiciones iniciales en 0)
filtered_ecg = lfilter(b, a, ecg_signal)

# Graficar ECG filtrado
plt.figure(figsize=(15, 4))
plt.plot(t, filtered_ecg)
plt.title('Señal ECG filtrada con filtro IIR')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (mV)')
plt.grid()
plt.show()
```
La ecuación en diferencias describe cómo calcular la salida del filtro en función de las entradas actuales y pasadas, así como de las salidas anteriores. Es esencial para implementar el filtro en sistemas digitales, ya que reemplaza las operaciones en el dominio de la frecuencia por una forma iterativa en el tiempo.De lo anterior se obtuvo la siguiente ecuación:

![image](https://github.com/user-attachments/assets/03483db1-9813-4efc-9524-ea2d2eae365a)

La ecuación en diferencias obtenida a partir de los coeficientes b (numerador) y a (denominador) define cómo se calcula cada muestra de salida combinando entradas y salidas anteriores. La estructura del filtro muestra simetría (coeficientes impares el valor es 0) en los coeficientes, típica de un diseño pasa banda, y se encuentra normalizada (a[0]=1). Esta forma permite implementar el filtro de manera eficiente.

El filtro pasa banda de 0.1 Hz a 50 Hz con orden 4 es adecuado para procesar señales ECG porque elimina eficazmente la deriva de línea base (<0.5 Hz) y el ruido de alta frecuencia (>50 Hz), incluyendo interferencia de red y artefactos musculares, mientras conserva las componentes fisiológicas clave como las ondas P, QRS y T. El diseño IIR de orden moderado (4) ofrece una buena atenuación con baja exigencia computacional.Luego de aplicar el filtro a la señal se obtuvo lo siguiente

![image](https://github.com/user-attachments/assets/eda80515-0d4a-4c16-95e5-d0218343f7b3)

#### Detección de los Picos R

```bash
peaks, _ = find_peaks(filtered_ecg, distance=0.6*fs, height=np.std(filtered_ecg))  ## La función find_peaks busca los picos (máximos locales) en la señal filtered_ecg, distance=0.6*fs parámetro distance especifica la distancia mínima entre los picos en número de muestras. Se establece como el 60% de la frecuencia de muestreo (fs), lo cual ayuda a evitar que se detecten picos demasiado cercanos, que podrían corresponder a artefactos,height=np.std(filtered_ecg): parámetro asegura que solo se detecten picos cuya amplitud sea superior a la desviación estándar de la señal. Esto ayuda a eliminar picos pequeños que no corresponden a eventos significativos.peaks, _: La función devuelve dos valores. El primero, peaks, es un array que contiene los índices de los picos detectados en la señal. El segundo valor, _, es el cual no estamos utilizando en este caso.

rpeak_times = peaks / fs ## convierte los índices de los picos detectados en tiempos (en segundos). La conversión se hace dividiendo el índice de cada pico por la frecuencia de muestreo fs.
rr_intervals = np.diff(rpeak_times) * 1000  # ms , La función np.diff() calcula la diferencia entre los elementos consecutivos en el array rpeak_times, es decir, calcula los intervalos R-R (el tiempo entre picos R consecutivos).* 1000: Convierte los intervalos R-R de segundos a milisegundos.

# Graficar picos R
plt.figure(figsize=(15, 4))
plt.plot(t, filtered_ecg)
plt.plot(peaks / fs, filtered_ecg[peaks], "rx") ## pone una x en cada pico
plt.title('Detección de Picos R')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (mV)')
plt.grid()
plt.show()
```
De lo anterior se obtuvo la siguiente gráfica,donde Se puede observara que los picos R se demarcaron con una x

![image](https://github.com/user-attachments/assets/c179e8a7-a821-4708-9f88-b9992433f2ca)

## Análisis de la HRV en el dominio del tiempo
```bash
mean_rr = np.mean(rr_intervals)  # np.mean() calcula la media (promedio) de los intervalos R-R, promedio de los tiempos entre picos R consecutivos
std_rr = np.std(rr_intervals)  # np.std() calcula la desviación estándar de los intervalos R-R, que mide la dispersión o variabilidad entre los intervalos

print(f"Media RR: {mean_rr:.2f} ms")  # Imprime la media de los intervalos R-R en milisegundos, con un formato de dos decimales
print(f"Desviación estándar RR: {std_rr:.2f} ms")  # Imprime la desviación estándar de los intervalos R-R en milisegundos, con un formato de dos decimales

plt.figure(figsize=(12, 4))  # Define el tamaño de la figura de la gráfica: 12 unidades de ancho y 4 de alto
plt.plot(rr_intervals, marker='o')  # Dibuja los intervalos R-R a lo largo del eje X, representados por círculos en la gráfica
plt.axhline(mean_rr, color='red', linestyle='--', label='Media RR')  # Dibuja una línea horizontal en la posición de la media de los intervalos R-R. La línea es roja y discontinua.

plt.title('Intervalos RR')  # Define el título de la gráfica como 'Intervalos RR'
plt.xlabel('Latido')  # Etiqueta el eje X indicando que representa los latidos de corazón, o los eventos R-R
plt.ylabel('Intervalo RR (ms)')  # Etiqueta el eje Y indicando que representa los intervalos R-R en milisegundos
plt.legend()  # Añade una leyenda a la gráfica para explicar los elementos visuales (en este caso, la línea de la media RR)
plt.grid()  # Añade una cuadrícula a la gráfica para facilitar la lectura de los valores
plt.show()  # Muestra la figura de la gráfica generada en pantalla

```
Aplicando lo anterior se obtuvo:

![image](https://github.com/user-attachments/assets/3e2de52f-9069-4fcb-b0e3-c098b3676c5e)

El análisis de tiempo continuo muestra una media del intervalo RR de 806.71 ms, lo que equivale a una frecuencia cardíaca promedio de aproximadamente 74 latidos por minuto (usando la formula 60000/RR promedio), dentro del rango normal en reposo. La desviación estándar de los intervalos RR es de 122.16 ms, lo cual indica una variabilidad de la frecuencia cardíaca (HRV) alta, generalmente asociada con un buen estado de salud cardiovascular y un equilibrio adecuado del sistema nervioso autónomo, especialmente con predominio parasimpático. Esta alta variabilidad suele observarse en personas con buena condición física y bajo nivel de estrés. Esto indicaría que en la mayor parte del experimento el sujeto se mantuvo tranquilo y que en espacios muy cortos de tipo o finalizando dicho proceso experimento estimulo simpático brevemente.


![image](https://github.com/user-attachments/assets/68028753-8d53-4496-ad61-80534ef866d6)

La gráfica representa los intervalos RR extraídos de la señal, mostrando la variación temporal del tiempo entre latidos consecutivos. La línea roja discontinua indica la media general, cercana a 807 ms, lo que corresponde a una frecuencia cardíaca promedio normal. La mayoría de los intervalos se agrupan alrededor de este valor, lo que sugiere una buena variabilidad de la frecuencia cardíaca (HRV), indicador de un sistema nervioso autónomo funcional y equilibrado. Sin embargo, se observan varios picos anómalos, especialmente hacia el final de la señal, que superan los 1600 ms y podrían deberse a errores en la detección de picos R o artefactos en la señal. Estas irregularidades deben ser consideradasya que pueden afectar la calidad de la información tratada.









