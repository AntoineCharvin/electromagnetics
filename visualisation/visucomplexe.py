import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 101)
z = np.exp(-1j*2*np.pi*x) + np.exp(-x**2)

X = np.array([x,x])

y0 = np.zeros(len(x))
y = np.abs(z)
Y = np.array([y0,y])

Z = np.array([z,z])
C = np.angle(Z)

plt.plot(x, y, "k")

plt.pcolormesh(X, Y, C, shading="gouraud", cmap=plt.cm.hsv, vmin=-np.pi, vmax=np.pi)
plt.colorbar()

plt.show()
