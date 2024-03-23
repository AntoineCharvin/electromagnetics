import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Définition de la fonction f(x, y)
def f(x, y):
    return np.log(3 * x**2 + y**2 + 1)

# Génération des points dans l'intervalle [-2, 7] avec des espacements de 0.2 dans la direction x
# et de 0.5 dans la direction y
x_values = np.arange(-2, 7.2, 0.2)
y_values = np.arange(-2, 7.5, 0.5)

# Création d'une grille de points à partir des valeurs de x et y
x, y = np.meshgrid(x_values, y_values)

# Calcul des valeurs de la fonction f(x, y) pour chaque point de la grille
z = f(x, y)

# Tracé de la fonction en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')

# Ajout d'étiquettes et de titres
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')
ax.set_title('Graphique de la fonction f(x, y)')

# Affichage du graphique
plt.show()
