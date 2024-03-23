#nom: CHARVIN
#prenom: Antoine
#Exercice 1g

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Number of time steps
nbt = 2000

# Courant stability factor
S = 1

# Speed of light
c = 2.99792458e8

# Wavelength of the incident light
lambda0 = 1.55e-6

# Number of wavelengths to consider
Nlambda = 21

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
indice_dielec = 1.9
centre_dielec = (xmax - xmin) / 2
largeur_dielec = 12*lambda0

# Set the dielectric constant within the region of the interface
list_dielec_indices = []
for i in range(nbx):
    if (abs(x[i] - centre_dielec) < largeur_dielec/2):
        epsilon_r[i] = indice_dielec**2
        list_dielec_indices.append(i)

#initialize amplitude before and after the interface to calculate the reflection and transmission coefficients
start_dielec = list_dielec_indices[0]
end_dielec = list_dielec_indices[-1]
max_amplitude_after_interface = 0
max_amplitude_before_interface = 0

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
tc=8.2*T
tau=2.8*T

# Function for updating the plot at each time step
def animate(n):
    # Update the wave function at each spatial point
    for i in range(1, nbx-1):
        unp[i] = S**2 / epsilon_r[i] * (un[i+1] - 2*un[i] + un[i-1]) + 2*un[i] - unm[i]
        unp[-1] = 0

    # Define the source term
    tnp = (n+1) * dt

    

    if(n+1)*dt< (2 * tc):
        unp[0] = np.cos(W*(tnp-tc))*np.exp(-((tnp - tc)/(tau))**2)
    else:
        unp[0]=un[1]

    unp[-1]=un[-2]
    # Update the plot
    line.set_data(x, unp)

    global max_amplitude_before_interface, max_amplitude_after_interface
    #calculate the max amplitude before and after the interface to calculate the reflection and transmission coefficients
    max_amplitude_before_interface = sum(np.abs(unp[start_dielec:end_dielec]))
    max_amplitude_after_interface = sum(np.abs(unp[end_dielec+1:]))
    

    # Update the wave function arrays
    unm[:] = un[:]
    un[:] = unp[:]

    return line,

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=nbt, interval=0.001, blit=True, repeat=False)

# Display the plot
plt.show()

# calculate the numerical reflection and transmission coefficients
transmission_coefficient = max_amplitude_after_interface  / (max_amplitude_before_interface + max_amplitude_after_interface)
print("computed transmission coefficient:", transmission_coefficient)
print("computed reflection coefficient:", 1 - transmission_coefficient)

#analytical solution
fresnel_transmission_coefficient = (4 * indice_dielec) / ((1 + indice_dielec)**2)
print("fresnel transmission coefficient:", fresnel_transmission_coefficient)
fresnel_reflection_coefficient = ((1 - indice_dielec)**2) / ((1 + indice_dielec)**2)
print("fresnel reflection coefficient:", fresnel_reflection_coefficient)