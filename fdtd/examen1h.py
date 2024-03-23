import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

lambda0 = 1.55e-6  # Wavelength in meters
N_lambda = 20      # Number of grid points per wavelength
dx = lambda0 / N_lambda

c = 2.99792458e8  # Speed of light in vacuum
mu0 = np.pi * 4e-7
eps0 = 1 / (mu0 * c**2)

S = 1  # Courant number
dt = S * dx / c  # Time step
T = lambda0 / c  # Period of the wave

nbez = 40 * N_lambda
nbhy = nbez - 1
xmin = 0
xmax = (nbez - 1) * dx

ez = np.zeros(nbez)   # Electric field Ez
hy = np.zeros(nbhy)   # Magnetic field Hy

xez = np.linspace(xmin, xmax, nbez)
xhy = np.linspace(xmin + dx/2, xmax - dx/2, nbhy)

# Medium properties
indice2 = 2.1  # Refractive index of the second medium
centre_dielec = (xmax - xmin) / 2
largeur_dielec = lambda0 * 9.7

# Refractive index array
indice = np.ones(nbez)
for i in range(nbez):
    if abs(xez[i] - centre_dielec) < largeur_dielec / 2:
        indice[i] = indice2

# Permittivity and permeability arrays
eps = eps0 * indice**2
mu = mu0 * np.ones(nbhy)

# Update coefficients
ca = np.ones(nbez)
cb = dt / (dx * eps)
da = np.ones(nbhy)
db = dt / (dx * mu)

nbt = 2000  # Number of time steps

fig = plt.figure()
plt.vlines(centre_dielec-largeur_dielec/2, -1.5, 2.1, color='r', linestyle='--')
plt.vlines(centre_dielec+largeur_dielec/2, -1.5, 2.1, color='r', linestyle='--')
line, = plt.plot(xez, ez)
plt.ylim(-1.5, 2.1)

def animate(n):
    tnp = (n + 1) * dt
    # Source field
    ez[0] = np.cos(2 * np.pi / T * tnp) * np.exp(-((tnp - 10 * T) / (4 * T))**2)
    # Update fields using Yee algorithm
    for i in range(1, nbez - 1):
        ez[i] = cb[i] * (hy[i] - hy[i - 1]) + ca[i] * ez[i]
    for i in range(nbhy):
        hy[i] = db[i] * (ez[i + 1] - ez[i]) + da[i] * hy[i]
    
    #perfect metal boundary condition
    ez[-1] = 0
    hy[-1] = 0

    line.set_data(xez, ez)
    return line,

ani = animation.FuncAnimation(fig, animate, frames=nbt, blit=True, interval=1, repeat=False)

plt.show()
