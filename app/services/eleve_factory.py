from app.models.eleve import Eleve, ElevePoleDance

class EleveFactory:
    @staticmethod
    def create_eleve(type_eleve, nom, email, niveau=None):
        if type_eleve == "eleve_pole":
            return ElevePoleDance(nom, email, niveau)
        elif type_eleve == "eleve":
            return Eleve(nom, email)
        else:
            raise ValueError(f"Type d'élève inconnu: {type_eleve}")
