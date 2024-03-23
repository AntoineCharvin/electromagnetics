class Livre:
    def __init__(self, titre, auteur, nb_pages):
        self._titre = titre
        self._auteur = auteur
        self._nb_pages = nb_pages 

    @property
    def titre(self):
        return self._titre
    
    @titre.setter
    def titre(self, titre):
        self._titre = titre

    @property
    def nb_pages(self):
        return self._nb_pages
    
    @nb_pages.setter
    def nb_pages(self, nb_pages):
        if nb_pages > 0:
            self._nb_pages = nb_pages
        else:
            print("Erreur : Le nombre de pages doit être positif.")

    @property
    def auteur(self):
        return self.auteur

    @auteur.setter
    def auteur(self, auteur):
        self._auteur = auteur

    def affiche(self):
        print(f"Titre: {self._titre}")
        print(f"Auteur: {self._auteur}")
        print(f"Nombre de pages: {self._nb_pages}")

    

    

# Programme principal
livre1 = Livre("Livre 1", "Auteur 1", 200)
livre2 = Livre("Livre 2", "Auteur 2", 300)

# Afficher les informations sur les livres
livre1.affiche()
livre2.affiche()

# Modifier le nombre de pages de chaque livre
livre1.nb_pages = 250
livre2.nb_pages = 350

# Afficher les nombres de pages mis à jour
print(f"Nombre de pages de {livre1.titre}: {livre1.nb_pages}")
print(f"Nombre de pages de {livre2.titre}: {livre2.nb_pages}")

# Calculer et afficher le nombre total de pages des deux livres
total_pages = livre1.nb_pages + livre2.nb_pages
print(f"Nombre total de pages des deux livres : {total_pages}")
