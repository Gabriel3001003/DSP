import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib.cm as cm

fs = 20 
f0 = 1 
f1 = 5

n = np.arange(0, 199)
n2 = np.arange(0, 99)

x1 = np.sin(2*np.pi*(f0/fs)*n) + np.sin(2*np.pi*(f1/fs)*n)

x2 = np.concatenate([np.sin(2*np.pi*(f0/fs)*n), np.sin(2*np.pi*(f1/fs)*n2)])

plt.figure(1)
plt.plot(x1)
plt.grid(True)
plt.figure(2)
plt.plot(x2)
plt.grid(True)

N = 1000
f = np.arange(-N/2, N/2) * (fs/N)
X1 = np.fft.fftshift(np.fft.fft(x1,N))
plt.figure(3)
plt.plot(f, np.abs(X1))
plt.title('Espectro suma de senoidales')
plt.grid(True)

X2 = np.fft.fftshift(np.fft.fft(x2,N))
plt.figure(4)
plt.plot(f, np.abs(X2))
plt.title('Espectro señales concatenadas')
plt.grid(True)

#espectrogramas
plt.figure(5)
f_spec, t_spec, Sxx = signal.spectrogram(x1, fs=fs, nperseg=20)
plt.pcolormesh(t_spec, f_spec, Sxx, shading ='gouraud')
plt.ylabel ('Frecuencia en Hz')
plt.xlabel('Tiempo [s]')
plt.title('Espectrogra,a de la suma de senoides')
plt.colorbar(label = "Densidad de potencia")

plt.figure(6)
f_spec2, t_spec2, Sxx2 = signal.spectrogram(x2, fs=fs, nperseg=20)
plt.pcolormesh(t_spec2, f_spec2, Sxx2, shading ='gouraud')
plt.ylabel ('Frecuencia en Hz')
plt.xlabel('Tiempo [s]')
plt.title('Espectrogra,a de senoides concatenadas')
plt.colorbar(label = "Densidad de potencia")

fig = plt.figure(7)
ax = fig.add_subplot(111, projection = '3d')
T,F = np.meshgrid(t_spec2, f_spec2)
surf = ax.plot_surface(T,F,Sxx2, cmap = cm.coolwarm)
ax.set_xlabel('tiempo')
ax.set_ylabel('Frecuencia')
ax.set_zlabel('Potencia')
fig.colorbar(surf, ax = ax, aspect = 5)


plt.show()