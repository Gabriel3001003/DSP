import numpy as np
import matplotlib.pyplot as plt

#frecuencia de oscilación 
f0 = 100
#Frecuencia de muestreo
fs = 1000
#Muestras disponibles
N= 1000

#eje del tiempo
n = np.arange(0,N)
x = np.cos(2*np.pi *(f0/fs)*n)

N1 = 1000 #Numero de puntos de la TDF

#Calcular la transformada de fourier
X = np.fft.fft(x, N1)
Xshift = np.fft.fftshift(X)
f = np.arange(-N/2, N1/2)*(fs/N1)

#Grafica 1 magnitud del espectro
plt.figure(1)
plt.plot(f, np.abs(Xshift))
plt.xlabel('Frecuencia en Hz')
plt.ylabel('|X(k)|')
plt.title('Magnitud de  X(k)')
plt.grid(True)

#Grafica 2 magnitud normalizada del espectro
plt.figure(2)
plt.plot(f,(1/N)*np.abs(Xshift))
plt.xlabel('Frecuencia en Hz')
plt.ylabel('|X(k)| Normalizada')
plt.title('Magnitud normalizada de  X(k)')
plt.grid(True)

#Densidad espectral de potencia (PSD)
Sxx = (1/N) * np.abs(X)**2
#Centrar la señal
Sxx_shift = np.fft.fftshift(Sxx)

#Grafica 3 PSD del espectro
plt.figure(3)
plt.plot(f,Sxx_shift)
plt.xlabel('Frecuencia en Hz')
plt.ylabel('Magnitud al cuadrado de |X(k)|')
plt.title('PSD de la señal senoidal')
plt.grid(True)

#PSD en Escala logaritmica (decibeles)
Sxx_db = 10 * np.log10(Sxx_shift)

#Grafica 4 PSD 
plt.figure(4)
plt.plot(f,Sxx_db)
plt.xlabel('Frecuencia en Hz')
plt.ylabel('Magnitud al cuadrado de X(k)')
plt.title('PSD de la señal senoidal en Db')
plt.grid(True)
plt.show()