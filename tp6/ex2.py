class PointAxe:
    def __init__(self, nom, abscisse):
        self.nom = nom
        self.abscisse = abscisse

    def affiche(self):
        print(f"Point {self.nom} - Abscisse : {self.abscisse}")

    def translate(self, valeur_translation):
        self.abscisse += valeur_translation
