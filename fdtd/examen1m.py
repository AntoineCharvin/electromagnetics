#nom: Dhungana
#prenom: Nischal
#Exercice 1a

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


#measure the speed of wave inside medium and outside medium
# Define two positions in air and two in the medium
pos_air_1, pos_air_2 = 5 * lambda0, 10 * lambda0
pos_medium_1, pos_medium_2 = centre_dielec - largeur_dielec/4, centre_dielec + largeur_dielec/4

# Variables to track the times
time_air_1 = time_air_2 = time_medium_1 = time_medium_2 = speed_air = speed_medium = None

# Indexes for the positions
index_air_1 = np.argmin(np.abs(x - pos_air_1))
index_air_2 = np.argmin(np.abs(x - pos_air_2))
index_medium_1 = np.argmin(np.abs(x - pos_medium_1))
index_medium_2 = np.argmin(np.abs(x - pos_medium_2))

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

    # Update the wave function arrays
    unm[:] = un[:]
    un[:] = unp[:]

    global time_air_1, time_air_2, time_medium_1, time_medium_2, speed_air, speed_medium  # Declare these as global variables

    #Measure the speed of wave inside medium and outside medium
     # Detect wavefront passage and record time
    if unp[index_air_1] > 1e-9 and time_air_1 is None:
        time_air_1 = n * dt
    if unp[index_air_2] > 1e-9 and time_air_2 is None:
        time_air_2 = n * dt
    if unp[index_medium_1] > 1e-9 and time_medium_1 is None:
        time_medium_1 = n * dt
    if unp[index_medium_2] > 1e-9 and time_medium_2 is None:
        time_medium_2 = n * dt

    # Calculate speeds if times are recorded
    if time_air_2 and time_air_1:
        speed_air = (pos_air_2 - pos_air_1) / (time_air_2 - time_air_1)
    if time_medium_2 and time_medium_1:
        speed_medium = (pos_medium_2 - pos_medium_1) / (time_medium_2 - time_medium_1)

    return line,

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=nbt, interval=1, blit=True, repeat=False)

# Display the plot
plt.show()

# Compare speeds and print ratio
if speed_air and speed_medium:
    print(f"Speed Ratio (Medium/Air): {speed_air/speed_medium}")





