import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#amélioration en changeant S, la largeur de la gaussienne et N_lambda

c = 2.99792458e8

nbt = 10000 #durée de la simulation pour l'animation
S = 1 

lambda0 = 1.55e-6
N_lambda = 30
dx = lambda0 / N_lambda

dt = S * dx / c

largeur_simul = 30 * lambda0 
nbx = int(largeur_simul / dx) + 1

T = lambda0 / c

xmin = 0
xmax = xmin + (nbx - 1) * dx #nbr intervales = nbr points - 1
x = np.linspace(xmin, xmax, nbx)

#initialisation
unm = np.zeros(nbx) #instant n moins 1
un = np.zeros(nbx) # instant n
unp = np.zeros(nbx) #insatnt n plus 1


indice = np.ones(nbx)
for i in range(nbx):
    if i > nbx / 2:
        indice[i] = 1.45
        
eps_r = indice**2


fig = plt.figure() # initialise la figure
line, = plt.plot([], [])
plt.plot(x, indice)
plt.xlim(xmin, xmax)
plt.ylim(-2, 2)



def animate(n): 
    tnp = (n+1) * dt
    
    for i in range(1, nbx-1):
        unp[i]= S**2 / eps_r[i] * (un[i+1] - 2*un[i] + un[i-1]) +2*un[i] - unm[i] 
        
    unp[0]=np.cos( (2*np.pi*(tnp-8*T)/T) ) * np.exp( - ((tnp - 8*T)/ (3*T))**2)
        
    line.set_data(x, unp)
    
    unm[:] = un[:] 
    un[:] = unp[:]
    
    return line,
 
ani = animation.FuncAnimation(fig, animate, frames=nbt, blit=True, interval=1, repeat=False)

plt.show()


#interprétation
# deux phénomènes: transmission et réflexion
# max reflexion en bas, 
#max transmission reste en haut, 

