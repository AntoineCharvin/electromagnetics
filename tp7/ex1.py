class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def deplace(self, dx, dy):
        self.__x = self.__x + dx
        self.__y = self.__y + dy

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

class PointA(Point):
    def affiche(self):
        print(f"Coordonnées du point : ({self.get_x()}, {self.get_y()})")

# Création d'un objet de la classe PointA
point = PointA(3, 4)

# Appel de la méthode affiche() pour afficher les coordonnées
point.affiche()


# Si la classe Point ne disposait pas des méthodes get_x() et get_y(), 
# vous ne pourriez pas accéder directement aux coordonnées x et y 
# d'un objet de la classe Point. Cela signifierait que vous ne pourriez 
# pas obtenir ces valeurs en dehors de la classe, ce qui limiterait la convivialité 
# et l'utilité de la classe. En conséquence, la classe PointA ne pourrait pas utiliser 
# ces méthodes pour afficher les coordonnées dans la méthode affiche(), et cela 
# entraînerait une erreur ou un comportement non souhaité.
