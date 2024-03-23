import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Paramètres
x_min, x_max = -3, 13
t_min, t_max = 0, 4
num_x_points, num_t_points = 161, 41

# Génération des points dans les intervalles spécifiés
x_values = np.linspace(x_min, x_max, num_x_points)
t_values = np.linspace(t_min, t_max, num_t_points)

# Création de la figure et de l'axe
fig, ax = plt.subplots()


line, = ax.plot([], [], lw=2)

# Ajout d'étiquettes et de titres
ax.set_xlim(x_min, x_max)
ax.set_ylim(0, 1)
ax.set_xlabel('x')
ax.set_ylabel('f(x, t)')
ax.set_title('Animation temporelle de f(x, t)')


def update(frame):
    t = t_values[frame]
    y_values = 1 / (1 + (x_values - 4.8 * t)**2)
    line.set_data(x_values, y_values)
    return line,

# Création de l'animation
animation = FuncAnimation(fig, update, frames=num_t_points, blit=True, interval=20)

# Affichage de l'animation
plt.show()
