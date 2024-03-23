sig= np.zeros(nbez)
for i in range(nbez):
    if abs(xez[i] - centre_dielec) < largeur_dielec / 2:
        sig[i] = 3000

sim = np.zeros(nbhy)

ca = (1-sig*dt/(2*eps)) / (1+sig*dt/(2*eps))
cb = dt/(dx*eps) / (1+sig*dt/(2*eps))  
da = (1-sim*dt/(2*mu)) / (1+sim*dt/(2*mu))
db = dt/(dx*mu) / (1+sim*dt/(2*mu))