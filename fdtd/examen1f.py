#nom: CHARVIN
#prenom: Antoine
#Exercice 1f

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Number of time steps
nbt = 1500

# Courant stability factor
S = 1

# Speed of light
c = 2.99792458e8

# Wavelength of the incident light
lambda0 = 1.55e-6

# Number of wavelengths to consider
Nlambda = 32

# Calculate the spatial step size
dx = lambda0 / Nlambda

# Calculate the time step size
dt = S * dx / c

# Define the spatial domain
xmin = 0
xmax = 22 * lambda0

# Calculate the number of spatial steps
nbx = int((xmax - xmin) / dx)

# Create an array of spatial coordinates
x = np.linspace(xmin, xmax, nbx)

# Calculate the period of the incident light
T = lambda0 / c

# Calculate the angular frequency of the incident light
W = 2 * np.pi / T

# Initialize the arrays for the wave function at three consecutive time steps
unm = np.zeros(nbx)
un = np.zeros(nbx)
unp = np.zeros(nbx)

# Parameters for the dielectric interface
epsilon_r = np.ones(nbx)

# Positioning of the first dielectric interface
indice_dielec1 = np.sqrt(2.1)
start_dielec1 = 10 * lambda0
largeur_dielec1 = lambda0 / 4

# Positioning of the second dielectric interface
indice_dielec2 = 2.1
start_dielec2 = start_dielec1 + largeur_dielec1
largeur_dielec2 = lambda0 * 9.7

# Set the dielectric constant within the region of the interfaces
for i in range(nbx):
    if start_dielec1 <= x[i] < start_dielec1 + largeur_dielec1:
        epsilon_r[i] = indice_dielec1**2
    if start_dielec2 <= x[i] < start_dielec2 + largeur_dielec2:
        epsilon_r[i] = indice_dielec2**2

# Create a figure for plotting
fig = plt.figure()

# Plot the dielectric constant
plt.plot(x, epsilon_r)

# Create an empty line for the wave function
line, = plt.plot([], [])

# Set the x and y limits of the plot
plt.xlim(xmin, xmax)
plt.ylim(-2, max(epsilon_r) +0.1)

#define for the source term
tc=8*T
tau=3*T


# Function for updating the plot at each time step
def animate(n):
    # Update the wave function at each spatial point
    for i in range(1, nbx-1):
        unp[i] = S**2 / epsilon_r[i] * (un[i+1] - 2*un[i] + un[i-1]) + 2*un[i] - unm[i]
  
    # Define the source term
    tnp = (n+1) * dt

    if(n+1)*dt< (2 * tc):
        unp[0] = np.cos(W*tnp)*np.exp(-((tnp - tc)/(tau))**2)
    else:
        unp[0]=un[1]

    unp[-1]=un[-2]

    # Update the plot
    line.set_data(x, unp)

    # Update the wave function arrays
    unm[:] = un[:]
    un[:] = unp[:]

    return line,

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=nbt, interval=10, blit=True, repeat=False)

# Display the plot
plt.show()