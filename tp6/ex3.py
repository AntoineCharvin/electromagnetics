class Point:
    origine = 0
    def __init__(self, nom, abs_absolue) :
        self.nom = nom
        self.abs_absolue = abs_absolue

    def affiche(self):

        print(f"Point {self.nom} - abscisse = {self.abs_absolue - Point.origine}")
        print(f"\trelative à une origine d'abscisse absolue {Point.origine}")


    @classmethod
    def set_origine(cls, o):
        Point.origine = o

    @classmethod
    def get_origine(self):
        return Point.origine


# Programme principal
a = Point('A', 3)
a.affiche()

b = Point('B', 6)
b.affiche()
print('-------------------------------------------------------------')
print('-------------------------------------------------------------')
a.set_origine(2)
print("On a placé l'origine en", a.get_origine())

a.affiche()
b.affiche()
