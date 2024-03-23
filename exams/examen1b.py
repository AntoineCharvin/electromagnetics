#nom: CHARVIN
#prenom: Antoine
#Exercice 1b

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Number of time steps
nbt = 1000

# Courant stability factor
S = 0.3

# Speed of light
c = 2.99792458e8

# Wavelength of the incident light
lambda0 = 1.55e-6

# Number of wavelengths to consider
Nlambda = 14

# Calculate the spatial step size
dx = lambda0 / Nlambda

# Calculate the time step size
dt = S * dx / c

# Define the spatial domain
xmin = 0
xmax = 9 * lambda0

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

# Create a figure for plotting
fig = plt.figure()

# Create an empty line for the wave function
line, = plt.plot([], [])

# Set the x and y limits of the plot
plt.xlim(xmin, xmax)
plt.ylim(-1.4, 1.4)

#define for the source term
tc=2.5*T
tau=0.9*T

# Function for updating the plot at each time step
def animate(n):
    # Update the wave function at each spatial point
    for i in range(1, nbx-1):
        unp[i] = S**2 / epsilon_r[i] * (un[i+1] - 2*un[i] + un[i-1]) + 2*un[i] - unm[i]
        unp[-1] = 0
    # Define the source term
    tnp = (n+1) * dt

    unp[0] = np.cos(W*(tnp-tc))*np.exp(-((tnp - tc)/(tau))**2)

    # Update the plot
    line.set_data(x, unp)

    # Update the wave function arrays
    unm[:] = un[:]
    un[:] = unp[:]

    return line,

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=nbt, interval=20, blit=True, repeat=False)

# Display the plot
plt.show()