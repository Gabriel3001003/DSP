import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

#datos calculados
M = 27
wc = 0.45*np.pi

n = np.arange(-(M-1)//2, (M-1)//2 + 1)
#paso 2: Calcular la respuesta al impulso ideal
h_ideal = (wc/np.pi) * np.sinc(wc*n /np.pi)

#paso 3: APlicar la ventana seleccionada (hanning) 
window = np.hanning(M)
h_truncada = h_ideal * window

#calcular la respuesta en frecuencia 
w, H = signal.freqz(h_truncada, 1, worN = 1024)
w_normalizada = w/ np.pi
H_magnitud = np.abs(H)
H_db = 20 * np.log10(H_magnitud + 1e-10)


plt.figure(1)
plt.stem(n,h_ideal, 'b', markerfmt='bo', label ='Ideal')
plt.stem(n,h_truncada,'r',markerfmt='ro', label = 'Truncada con ventana')
plt.xlabel('n [muestras]')
plt.ylabel('h[n]')
plt.title('respuesta al impulso')
plt.legend()
plt.grid(True)

plt.figure(2)
plt.plot(w_normalizada, H_magnitud)
plt.xlabel('w/pi[Rad/s]')
plt.ylabel('H(e^jw)')
plt.title('respuesta en frecuenica (magnitid)')
plt.legend()
plt.grid(True)

plt.figure(3)
plt.plot(w_normalizada, H_db)
plt.xlabel('w/pi[Rad/s]')
plt.ylabel('H(e^jw)|[db]')
plt.title('respuesta en frecuenica (db)')
plt.legend()
plt.grid(True)

plt.figure(4)
plt.plot(w_normalizada, H_magnitud)
plt.axvline(x= 0.3, color = 'g', linestyle = '--', label = 'wp = 0.3pi')
plt.axvline(x= 0.6, color = 'r', linestyle = '--', label = 'wc = 0.6pi')
plt.axhline(y = 0.99, color = 'm', linestyle= ':', label = 'delta_1 = 0.99')
plt.axhline(y = 0.99, color = 'm', linestyle= ':', label = 'delta_2 = 0.1')
plt.xlabel('w/pi[rad/s]')
plt.ylabel('H(e^jw)]')
plt.title('Verificación de especificaciones')
plt.legend(loc = 'best')
plt.grid(True)

plt.tight_layout()
plt.show()