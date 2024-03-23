import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return (np.sin(x) / x) * np.sqrt(x**2 + 1)

epsilon = np.finfo(float).eps
x = np.linspace(-6, 6, 121) + epsilon
y = f(x)

# Tracé de la fonction
plt.plot(x, y, label=r'$f(x) = \frac{\sin(x)}{x} \cdot \sqrt{x^2+1}$')

# Ajout d'étiquettes et de titres
plt.title('Graphique de la fonction')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()

plt.show()
