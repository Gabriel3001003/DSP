import numpy as np 
import matplotlib.pyplot as plt
from scipy.fft import fft

#Generacion de señal discreta en el tiempo
f0 = 100
f1 = 110
fs = 1000
N = 1000
n = np.arange(N)
#señal compuesta
x = np.cos(2*np.pi*(f0/fs)*n) + 0.005*np.cos(2*np.pi*(f1/fs)*n)
#obtener la transformada discreta de fourier
Xk = fft(x) #Calcular la transformada de fourier
f = n/N * fs
plt.plot (f, abs(Xk))
plt.title('Grafica de a magnitud del espectro')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Frecuencia del espectro $|X(\omega|$')
plt.show()