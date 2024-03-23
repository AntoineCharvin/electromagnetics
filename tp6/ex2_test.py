# Importer la classe PointAxe depuis le fichier point_axe.py
from ex2 import PointAxe

# Créer un point initial avec le nom "A" et l'abscisse 5
point_a = PointAxe("A", 5)

# Afficher les caractéristiques du point initial
print("Caractéristiques du point initial:")
point_a.affiche()

# Effectuer une translation du point en ajoutant 3 à son abscisse
point_a.translate(3)

# Afficher les caractéristiques du point après la translation
print("\nCaractéristiques du point après translation:")
point_a.affiche()
