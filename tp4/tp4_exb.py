from random import choice
import matplotlib.pyplot as plt

class Marcheur:
    def __init__(self):
        self.pos = [0]
    
    def walk(self, n):
        for i in range(n):
            pos_ant = self.get_pos()[len(self.get_pos())-1]
            self.pos.append(pos_ant+choice([-1,1]))
    
    def get_pos(self):
        return self.pos
    
    def get_pos_carre(self):
        pos_carre = []
        for i in range(len(self.get_pos())):
            pos_carre.append(self.get_pos()[i]**2)
        return pos_carre

m = Marcheur()
m.walk(1000)

plt.plot(m.get_pos_carre())
plt.show()