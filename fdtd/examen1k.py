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
# for i in range(nbez):
#     if abs(xez[i] - centre_dielec) < largeur_dielec / 2:
#         indice[i] = indice2

# Permittivity and permeability arrays
eps = eps0 * indice**2
mu = mu0 * np.ones(nbhy)

# construction du milieu pml
# debut_pml = 30 * lambda0
# eps_r_pml = 1   # cas de pml dans l'air
# mu_r_pml = 1    

# eps_pml = eps0 * eps_r_pml
# mu_pml  =  mu0 *  mu_r_pml
# eta_pml = np.sqrt( mu_pml/ eps_pml )

# # application de la formule 7.60a : sigma_x = (x/d)**m * sigma_x_max

# m = 3    # l'usage est d'avoir 3 <= m <=4 (voir au-dessus de la formule 7.62)
# d = 10*dx 

# # définition de sigma_x_max avec la formule 7.66 qui correspond à 10 couches
# sigma_x_max = 0.8 * (m+1) / ( eta_pml * dx )

# # definition de sigma_x
# def sigma_x(x):
#     return (x/d)**m * sigma_x_max

sig= np.zeros(nbez)
for i in range(nbez):
    if abs(xez[i] - centre_dielec) < largeur_dielec / 2:
        sig[i] = 3000

sim = np.zeros(nbhy)

ca = (1-sig*dt/(2*eps)) / (1+sig*dt/(2*eps))
cb = dt/(dx*eps) / (1+sig*dt/(2*eps))  
da = (1-sim*dt/(2*mu)) / (1+sim*dt/(2*mu))
db = dt/(dx*mu) / (1+sim*dt/(2*mu))

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

    line.set_data(xez, ez)
    return line,

ani = animation.FuncAnimation(fig, animate, frames=nbt, blit=True, interval=1, repeat=False)

plt.show()
