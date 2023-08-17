from personne import Personne

class Conseiller(Personne):
    tout = []

    def __init__(self, id=-1, nom="", statut=""):
        self.id = id
        self.nom = nom
        self.statut = statut
        self.equipes = []
        if (id not in [p.id for p in Conseiller.tout]):
            Conseiller.tout.append(self)