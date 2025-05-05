import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift

#a<1 para que se cumpla
#ejemplo con a = 0.8
a = 0.8
N = 100
fft_size = 1024 #Tamaño de la transformada de fourier

#Creamos la secuencia exponencial.
n = np.arange (N)
x = a**n 

#Calcular la transformada de fourier
X = fftshift (fft(x, fft_size))
omega = np.linspace (-np.pi, np.pi, fft_size)
X_calculada = 1 / (1- a *np.exp(-1j*omega))

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))


ax1.stem(n , x, basefmt = "b-")
ax1.set_title (f' Secuecnai exponencial $x[n = {a}^n u[n]$')
ax1.set_xlabel ('n')
ax1.set_ylabel('Amplitud')
ax1.grid(True)

ax2.plot(omega , np.abs(X_calculada), 'r-', label = 'Teorica')
ax2.plot (omega, np.abs(X)/ np.max(np.abs(X))*np.max(np.abs(X_calculada)), 'b--', label = 'Numerica (FFT)') 
ax2.set_title (f'magnitud de la TDF')
ax2.set_xlabel ('$\omega$ [rad/s]')
ax2.set_ylabel('Magnitud')
ax2.legend()
ax2.grid(True)
ax2.set_xlim([-4*np.pi, 4*np.pi])

#Grafica de la fase
ax3.plot(omega , np.angle(X_calculada), 'r-', label = 'Teorica')
ax3.plot (omega, np.angle(X),'b--', label = 'Numerica (FFT)') 
ax3.set_title (f'Fase de la TDF')
ax3.set_xlabel ('$\omega$ [rad/s]')
ax3.set_ylabel('Radianes')
ax3.legend()
ax3.grid(True)
ax3.set_xlim([-4*np.pi, 4*np.pi])
ax3.set_ylim([-np.pi, np.pi])

plt.tight_layout()
plt.show()