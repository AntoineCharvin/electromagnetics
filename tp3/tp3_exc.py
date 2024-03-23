import numpy as np


def est_matrice_identite(matrice):
    # Vérifie si la matrice est carrée (nombre de lignes = nombre de colonnes)
    if len(matrice) != len(matrice[0]):
        return False
    
    n = len(matrice)  # Obtient la taille de la matrice (nombre de lignes/colonnes)
    
    # Parcourt la matrice pour vérifier si elle est une matrice identité
    for i in range(n):
        for j in range(n):
            if i == j:
                # Sur la diagonale principale, les éléments doivent être égaux à 1
                if matrice[i][j] < 0.99 and matrice[i][j] > 1.01:
                    return False
            else:
                # Hors de la diagonale principale, les éléments doivent être égaux à 0
                if matrice[i][j] < -0.01 and matrice[i][j] > 0.01:
                    return False
    
    # Si toutes les conditions sont satisfaites, la matrice est une matrice identité
    return True

sigy = np.array([[0, -1j],[1j, 0]])

valp, vecp = np.linalg.eig(sigy)
ket_u1 = vecp[0].reshape(2,1)
bra_u1 = ket_u1.transpose().conjugate()
ket_u2 = vecp[1].reshape(2,1)
bra_u2 = ket_u2.transpose().conjugate()

P1 = ket_u1.dot(bra_u1)
P2 = ket_u2.dot(bra_u2)

Id = P1 + P2
np.array(Id)
relation_fermeture = np.allclose(Id, np.eye(Id.ndim))
print("Relation de fermeture exacte : {}".format(relation_fermeture))


print("P1.P2 = {}".format(P1.dot(P2)))
print("P2.P1 = {}".format(P2.dot(P1)))


