import numpy as np
import scipy.fft as fft
import matplotlib.pyplot as plt

# Parámetros
f0 = 100  # Frecuencia de la señal en Hz
fs = 1000  # Frecuencia de muestreo en Hz
n = np.arange(1000)  # Vector de tiempo discreto

# Generación de la señal
x = np.cos(2 * np.pi * (f0 / fs) * n)

# Transformada Discreta de Fourier (FFT)
Xk = fft.fft(x)

# Gráfica del espectro de magnitud
plt.plot(np.abs(Xk))
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud')
plt.title('TDF de la señal con scipy.fft')
plt.show()
