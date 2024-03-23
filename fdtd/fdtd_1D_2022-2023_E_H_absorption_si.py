import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

lambda0 = 1.55e-6
N_lambda = 20
dx = lambda0 / N_lambda

c = 2.99792458e8
mu0 = np.pi*4e-7
eps0 = 1/(mu0*c**2)

S = 1
dt = S*dx/c
T = lambda0/c

nbez = 30 * N_lambda
nbhy = nbez - 1
xmin = 0 
xmax = (nbez-1) * dx

ez = np.zeros(nbez)   # Champ Ez
hy = np.zeros(nbhy) # Champ Hy

xez = np.linspace(xmin, xmax, nbez)
xhy = np.linspace(xmin+dx/2, xmax-dx/2, nbhy)

# indice du milieu 2
indice2 = 2

# définition du tableau pour les indices de refraction
indice = np.ones(nbez)
for i in range(nbez):
    if xez[i] > 15*lambda0:
        indice[i] = indice2

# définition des tableaux pour epsilon et mu
eps = eps0 * indice**2
mu = mu0 * np.ones(nbhy)

# construction du milieu pml
debut_pml = 25 * lambda0
eps_r_pml = indice2 **2   # cas de pml dans le milieu 2
mu_r_pml = 1    

eps_pml = eps0 * eps_r_pml
mu_pml  =  mu0 *  mu_r_pml
eta_pml = np.sqrt( mu_pml/ eps_pml )

# application de la formule 7.60a : sigma_x = (x/d)**m * sigma_x_max

m = 3    # l'usage est d'avoir 3 <= m <=4 (voir au-dessus de la formule 7.62)
d = 10*dx 

# définition de sigma_x_max avec la formule 7.66 qui correspond à 10 couches
sigma_x_max = 0.8 * (m+1) / ( eta_pml * dx )

# definition de sigma_x
def sigma_x(x):
    return (x/d)**m * sigma_x_max

sig= np.zeros(nbez)
for i in range(nbez):
    if xez[i] > debut_pml:
        sig[i] = sigma_x(xez[i]-debut_pml)

sim = np.zeros(nbhy)
for i in range(nbhy):
    if xhy[i] > debut_pml:
        sim[i] = sigma_x(xhy[i]-debut_pml) * mu_pml / eps_pml

ca = (1-sig*dt/(2*eps)) / (1+sig*dt/(2*eps))
cb = dt/(dx*eps) / (1+sig*dt/(2*eps))  
da = (1-sim*dt/(2*mu)) / (1+sim*dt/(2*mu))
db = dt/(dx*mu) / (1+sim*dt/(2*mu))  

nbt = 2000

fig = plt.figure() # initialise la figure
plt.plot(xez, indice) 
line, = plt.plot(xez, ez)
plt.ylim(-1.5, 2.1)

def animate(n):
    tnp = (n+1)*dt
    # champ de la source
    ez[0] = np.cos(2*np.pi/T*tnp)*np.exp(-( (tnp-10*T)/(4*T) )**2)
    # calcul du champ avec le schema numerique
    for i in range(1, nbez-1):
        ez[i] = cb[i] * (hy[i]-hy[i-1]) + ca[i] * ez[i]
    for i in range(nbhy):
        hy[i] = db[i] * (ez[i+1]-ez[i]) + da[i] * hy[i]
    line.set_data(xez, ez)
    return line,
 
ani = animation.FuncAnimation(fig, animate, frames=nbt, blit=True, interval=1, repeat=False)

plt.show()