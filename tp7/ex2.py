class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def aff_coord(self):
        print("Coordonnees : ", self.__x, self.__y)

class PointNom(Point):
    def __init__(self, x, y, nom):
        super().__init__(x, y)
        self.__nom = nom

    def aff_coord_nom(self):
        print(f"Coordonnees : ({self.get_x()}, {self.get_y()}), Nom : {self.__nom}")

# Création d'un objet de la classe PointNom
point_nom = PointNom(3, 4, "Point A")

# Appel de la méthode aff_coord_nom() pour afficher les coordonnées et le nom
point_nom.aff_coord_nom()
