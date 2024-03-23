import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

c = 2.99792458e8 #vitesse de la lumière

nbt = 1000 #durée de la simulation pour l'animation
S = 0.9 # facteur de stabilité


lambda0 = 1.55e-6 #longueur d'onde réelle
N_lambda = 20
dx = lambda0 / N_lambda

dt = S * dx / c 

largeur = 30 * lambda0
nbx = int(largeur / dx) + 1

T = lambda0 / c

xmin = 0
xmax = xmin + (nbx - 1) * dx #nbr intervales = nbr points - 1
x = np.linspace(xmin, xmax, nbx) #creation tableau des x

#initialisation des tableaux à zero
unm = np.zeros(nbx) #instant n - 1
un = np.zeros(nbx) # instant n
unp = np.zeros(nbx) #insatnt n + 1


fig = plt.figure()
line, = plt.plot([], []) 
plt.xlim(xmin, xmax)
plt.ylim(-2, 2)



def animate(n): 
    tnp = (n+1) * dt
    
    for i in range(1, nbx-1):
        unp[i]= S**2 * (un[i+1] - 2*un[i] + un[i-1]) +2*un[i] - unm[i] #équation d'onde avec méthode FDTD
        
    #équation de l'onde
    unp[0] = np.cos( (2*np.pi*(tnp-8*T)/T) ) * np.exp( - ((tnp - 8*T)/ (3*T))**2)
        
    line.set_data(x, unp)
    
    unm[:] = un[:] 
    un[:] = unp[:]
    
    return line,
 
ani = animation.FuncAnimation(fig, animate, frames=nbt, blit=True, interval=15, repeat=False)

plt.show()

