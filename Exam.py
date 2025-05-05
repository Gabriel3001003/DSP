import numpy as np 
import matplotlib.pyplot as plt 

# Parámetros de muestreo
frecuencia_muestreo = 512  # Frecuencia de muestreo en Hz
tiempo = np.arange(0, 1, 1/frecuencia_muestreo)  # Vector de tiempo de 1 segundo

# Señal compuesta por dos senoidales cercanas en frecuencia: 100 Hz y 104 Hz
senal = np.sin(2 * np.pi * 100 * tiempo) + np.sin(2 * np.pi * 104 * tiempo)

# Crear ventanas de análisis
longitud = len(senal)
ventana_hamming = np.hamming(longitud)
ventana_hanning = np.hanning(longitud)
ventana_blackman = np.blackman(longitud)

# Función para aplicar una ventana y calcular la FFT de la señal
def aplicar_ventana_y_fft(senal, ventana):
    senal_filtrada = senal * ventana  # Aplicar ventana
    espectro = np.fft.fft(senal_filtrada)  # Calcular la FFT
    frecuencias = np.fft.fftfreq(longitud, 1/frecuencia_muestreo)
    
    # Filtrar solo las frecuencias positivas
    frec_positivas = frecuencias[:longitud//2]
    magnitud = np.abs(espectro[:longitud//2])
    
    return frec_positivas, magnitud

# Calcular el espectro de magnitud para cada tipo de ventana
frec_hamming, mag_hamming = aplicar_ventana_y_fft(senal, ventana_hamming)
frec_hanning, mag_hanning = aplicar_ventana_y_fft(senal, ventana_hanning)
frec_blackman, mag_blackman = aplicar_ventana_y_fft(senal, ventana_blackman)

# Graficar los resultados
plt.figure(figsize=(10, 10))

plt.subplot(3, 1, 1)
plt.plot(frec_hamming, mag_hamming)
plt.title('Espectro de magnitud con ventana Hamming')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')

plt.subplot(3, 1, 2)
plt.plot(frec_hanning, mag_hanning)
plt.title('Espectro de magnitud con ventana Hanning')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')

plt.subplot(3, 1, 3)
plt.plot(frec_blackman, mag_blackman)
plt.title('Espectro de magnitud con ventana Blackman')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')

plt.tight_layout()
plt.show()

"""
Conclusión:

- Ventana Blackman: Mayor precisión espectral, ideal para separar frecuencias muy cercanas como 100 Hz y 104 Hz.
- Ventana Hamming: Buen equilibrio entre resolución y reducción de fugas, aunque con más solapamiento.
- Ventana Hanning: Similares resultados a Hamming, pero con menor supresión de lóbulos laterales.

Blackman es la mejor opción cuando se requiere alta resolución y mínima interferencia entre frecuencias.
"""
