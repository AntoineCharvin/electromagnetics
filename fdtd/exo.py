import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Paramètres de la simulation
nx = 200  
nt = 400    
s = 1
dt = 0.005  
c = 1
dx = c * dt / s

unp = np.zeros(nx)
un = np.zeros(nx)
unm = np.zeros(nx)

xmin = 0
xmax = xmin + (nx - 1) * dx # -1 car nb intervalles = nb point - 1
x = np.linspace(xmin, xmax, nx) 

t0 = 60*dt
tau = 20*dt

fig = plt.figure() # initialise la figure
line, = plt.plot([], []) 
plt.xlim(xmin, xmax)
plt.ylim(-2, 2)

def animate(n):
    tnp = (n+1) * dt

    for i in range(1, nx-1):
        unp[i]= s**2 * (un[i+1] - 2*un[i] + un[i-1]) + 2*un[i] - unm[i]

    unp[0]=np.exp( -( ((tnp-t0)/tau)**2))

    line.set_data(x, unp)

    unm[:] = un[:]
    un[:] = unp[:]

    return line,

anim = animation.FuncAnimation(fig, animate, frames=nt, blit=True, interval=20, repeat=True)
plt.show()