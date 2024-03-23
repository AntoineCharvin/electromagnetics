import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


c = 2.99792458e8

nbt = 3000  # durée de la simulation pour l'animation
S = 1

lambda0 = 1.55e-6
N_lambda = 30
dx = lambda0 / N_lambda

dt = S * dx / c

largeur_simul = 30 * lambda0
nbx = int(largeur_simul / dx) + 1

T = lambda0 / c

xmin = 0
xmax = xmin + (nbx - 1) * dx
x = np.linspace(xmin, xmax, nbx)

unm = np.zeros(nbx)  # instant n moins 1
un = np.zeros(nbx)  # instant n
unp = np.zeros(nbx)  # instant n plus 1

test1 = np.full((1, nbx), 0.8)
test2 = np.full((1, nbx), -0.2)
test3 = np.full((1, nbx), 0.2)
test4 = np.full((1, nbx), 0.16)
test5 = np.full((1, nbx), 0.93)

indice_lame = 1.45
largeur_lame = lambda0 / (2 * indice_lame)
centre_lame = x[int(nbx / 2)]

indice = np.ones(nbx)
in_lame = np.abs(x - centre_lame) < largeur_lame / 2
indice[in_lame] = indice_lame

eps_r = indice ** 2

fig, ax = plt.subplots()
line, = ax.plot([], [])
plt.plot(x, indice)
plt.xlim(xmin, xmax)
plt.ylim(-2, 2)


def animate(n):
    tnp = (n + 1) * dt

    unp[1:-1] = (S ** 2 / eps_r[1:-1] * (un[2:] - 2 * un[1:-1] + un[:-2]) + 2 * un[1:-1] - unm[1:-1])

    if tnp < 16 * T:
        unp[0] = np.cos((2 * np.pi * (tnp - 8 * T) / T)) * np.exp(-((tnp - 8 * T) / (3 * T)) ** 2)
    else:
        unp[0] = un[1]

    unp[-1] = un[-2]

    line.set_data(x, unp)

    unm[:] = un[:]
    un[:] = unp[:]

    return line,


ani = animation.FuncAnimation(fig, animate, frames=nbt, blit=True, interval=1, repeat=False)


plt.show()
