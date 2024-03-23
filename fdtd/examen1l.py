#nom: Dhungana
#prenom: Nischal
#Exercice 1a

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Number of time steps
nbt = 900

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
xmax = 30 * lambda0

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
indice_dielec = 2.1
centre_dielec = (xmax - xmin) / 2
largeur_dielec = lambda0 * 9.7

# Set the dielectric constant within the region of the interface
for i in range(nbx):
    if (abs(x[i] - centre_dielec) < largeur_dielec/2):
        epsilon_r[i] = indice_dielec**2

# Create a figure for plotting
fig = plt.figure()

# Plot the dielectric constant
plt.plot(x, epsilon_r)

# Create an empty line for the wave function
line, = plt.plot([], [])

# Set the x and y limits of the plot
plt.xlim(xmin, xmax)
plt.ylim(-1.4, 1.4)

#define for the source term
tc=8*T
tau=3*T

#measure lambda inside medium
start_index = np.where(x >= centre_dielec - largeur_dielec/2)[0][0]
end_index = np.where(x <= centre_dielec + largeur_dielec/2)[0][-1]

def measure_wavelength(unp, x, start, end):
    peaks = []
    for i in range(start, end-1):
        if unp[i-1] < unp[i] and unp[i+1] < unp[i]:
            peaks.append(x[i])
    
    if len(peaks) < 2:
        return 0
    
    wavelengths = [peaks[i+1] - peaks[i] for i in range(len(peaks)-1)]

    return np.mean(wavelengths)

wavelength_text = plt.text(0.5, 0.2, '', transform=fig.transFigure)

# Function for updating the plot at each time step
def animate(n):
    # Update the wave function at each spatial point
    for i in range(1, nbx-1):
        unp[i] = S**2 / epsilon_r[i] * (un[i+1] - 2*un[i] + un[i-1]) + 2*un[i] - unm[i]
        unp[-1] = 0
    # Define the source term
    tnp = (n+1) * dt

    unp[0] = np.cos(W*tnp)*np.exp(-((tnp - tc)/(tau))**2)

    # Update the plot
    line.set_data(x, unp)

    # Measure wavelength within the medium if enough cycles have passed
    threshold = 20
    if n > threshold:
        measured_lambda = 0
        max_measured_lambda = 0
        measured_lambda = measure_wavelength(unp, x, start_index, end_index)
        if measured_lambda > max_measured_lambda:
            max_measured_lambda = measured_lambda
            wavelength_text.set_text(f'Measured Wavelength: {max_measured_lambda:.2e} m')

    # Update the wave function arrays
    unm[:] = un[:]
    un[:] = unp[:]

    return line,

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=nbt, interval=1, blit=False, repeat=False)

# Display the plot
plt.show()