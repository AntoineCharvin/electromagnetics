class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def affiche(self):
        print("Coordonnees : ", self.__x, self.__y)

class PointNom(Point):
    def __init__(self, x, y, nom):
        super().__init__(x, y)
        self.__nom = nom

    def affiche(self):
        print("Coordonnees : ({}, {}), Nom : {}".format(self.get_x(), self.get_y(), self.__nom))

# Création d'une liste comprenant des objets de type Point et PointNom
liste_points = [
    Point(1, 2),
    PointNom(3, 4, "Point A"),
    Point(5, 6),
    PointNom(7, 8, "Point B")
]

# Utilisation d'une boucle pour appeler la méthode affiche pour chaque élément de la liste
for point in liste_points:
    point.affiche()
