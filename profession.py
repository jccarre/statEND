class Profession:
    tout = []

    def __init__(self, intitule=""):
        self.intitule = intitule
        self.personnes = []
        if(intitule not in [p.intitule for p in Profession.tout]):
            Profession.tout.append(self)