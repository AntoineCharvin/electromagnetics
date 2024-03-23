import matplotlib.pyplot as plt
import numpy as np
import random

# Coordonnées des sommets du triangle équilatéral
x = [0, 1, 0.5, 0]  # Les sommets forment un carré (temporaire)
y = [0, 0, np.sqrt(3)/2, 0]  # La hauteur du triangle équilatéral est sqrt(3)/2


# Tracer le triangle équilatéral
plt.plot(x, y, marker='o')
plt.fill(x, y, alpha=0.3)

ptx=0.3
pty=0.3

plt.scatter(ptx,pty)


random = np.randint


# Définir les limites de l'axe des x et y pour une meilleure apparence
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)

# Étiqueter les sommets du triangle
for i, (xi, yi) in enumerate(zip(x, y)):
    plt.text(xi, yi, f'({xi}, {yi:.2f})', ha='center', va='bottom')



# Titre et affichage
plt.title("Triangle Équilatéral avec un Point Arbitraire à l'Intérieur")
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.show()
