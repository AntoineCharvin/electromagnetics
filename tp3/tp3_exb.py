import numpy as np

sigy = np.array([[0, -1j],[1j, 0]])

valp, vecp = np.linalg.eig(sigy)
ket_u1 = vecp[0].reshape(2,1)
bra_u1 = ket_u1.transpose().conjugate()
ket_u2 = vecp[1].reshape(2,1)
bra_u2 = ket_u2.transpose().conjugate()



orthogonalité = np.allclose(bra_u1.dot(ket_u2), 0)
print(orthogonalité)


print("|u1> = {}".format(ket_u1))
print("|u2> = {}".format(ket_u2))
print("<u1|u1> = {}".format(bra_u1.dot(ket_u1)))
print("<u2|u2> = {}".format(bra_u2.dot(ket_u2)))
print("<u1|u2> = {}".format(bra_u1.dot(ket_u2)))