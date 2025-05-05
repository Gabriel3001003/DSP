import numpy as np
import matplotlib.pyplot as plt

def X_mag(omega, N) :
    num = np.sin(N*omega / 2)
    den = np.sin(omega / 2)
    return np.abs(num/den)

def X_fase (omega, N) : 
    return -omega*(N-1)/2

omega = np.linspace(-4*np.pi, 4*np.pi, 1000)
N = 5
plt.figure(figsize = (12,10))
plt.plot(omega, X_mag(omega, N))
plt.title ('Magnitud de X(w)')
plt.xlabel('W [rad/s]')
plt.ylabel('|X(w)|')
plt.grid()

plt.figure(figsize = (12,10))
plt.plot(omega, X_fase(omega, N))
plt.title ('Fase de X(w)')
plt.xlabel('W [rad/s]')
plt.ylabel('arg(X(w)) [Rad]')
plt.grid()

plt.tight_layout()
plt.show()