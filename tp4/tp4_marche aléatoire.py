import random
import matplotlib.pyplot as plt
import numpy as np

nb_pos=1000


nb_marcheur = 500
pos = np.zeros(nb_pos)
somme = np.zeros(nb_pos)

for marcheur in range(nb_marcheur):
    x=0
    for i in range(nb_pos):
        # Générer un nombre aléatoire entre 0 et 1 pour déterminer la direction (0 pour gauche, 1 pour droite)
        rand_direction = random.random()

        # Mettre à jour la position en x en fonction de la direction
        if rand_direction > 0.5:
            x -= 1  # Aller à gauche
        else:
            x += 1  # Aller à droite
        pos[i] = x
    somme += pos**2



t = range(nb_pos)

# Tracer la trajectoire en 1D
plt.plot(t, somme/nb_marcheur)
plt.xlabel("Nombre d'étapes")
plt.ylabel("Position en 1D")
plt.title("Marche aléatoire 1D ")
plt.grid(True)
plt.show()
