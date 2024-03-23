import numpy as np

def est_hermitique(mat):
    return np.array_equal(mat, mat.transpose().conjugate())

A = np.array([[0, -1j],[1j, 0]])

if est_hermitique(A):
    print("A est hermitique")
else:
    print("A n'est pas hermitiques")