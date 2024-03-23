import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

c = 1
nbx = 200 #domaine de la simulation, abscisse
nbt = 1000 #durée de la simulation pour l'animation
S = 1 #définit la forme de l'onde pour 1 fonction porte
dt = 0.1
dx = c * dt/S #formule cours S=cdt/dx

xmin = 0
xmax = xmin + (nbx - 1) * dx #nbr intervales = nbr points - 1
x = np.linspace(xmin, xmax, nbx) #creation tableau des x

#initialisation des tableaux à zero
unm = np.zeros(nbx) #instant n moins 1
un = np.zeros(nbx) # instant n
unp = np.zeros(nbx) #insatnt n plus 1


fig = plt.figure() # initialise la figure
line, = plt.plot([], []) 
plt.xlim(xmin, xmax)
plt.ylim(-2, 2)

def animate(n): 
    tnp = (n+1) * dt
    
    for i in range(1, nbx-1):#on elimine l'extrémitée gauche et droite car ces valeurs ne peuvent pas être calculées
        unp[i]= S**2 * (un[i+1] - 2*un[i] + un[i-1]) +2*un[i] - unm[i] 
        
    if tnp > 20*dt and tnp < 30*dt:
        unp[0] = 1
    else:
        unp[0] = 0
        
    line.set_data(x, unp)
    
    unm[:] = un[:] 
    un[:] = unp[:]
    
    return line,
 
ani = animation.FuncAnimation(fig, animate, frames=nbt, blit=True, interval=20, repeat=False)

plt.show()


