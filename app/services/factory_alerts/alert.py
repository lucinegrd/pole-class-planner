from datetime import datetime

class Alert:
    """Classe de base pour représenter une alerte."""

    def __init__(self, student=None, course=None):
        """Initialise une alerte avec un étudiant et/ou un cours."""
        self.student = student
        self.course = course
        self.timestamp = datetime.now()

    def get_type(self):
        """Retourne le type de l'alerte (doit être implémenté par les sous-classes)."""
        raise NotImplementedError()

    def get_message(self):
        """Retourne le message de l'alerte (doit être implémenté par les sous-classes)."""
        raise NotImplementedError()

    def get_actions(self):
        """Retourne les actions possibles pour l'alerte (doit être implémenté par les sous-classes)."""
        raise NotImplementedError()

    def to_dict(self):
        """Convertit l'alerte en dictionnaire pour affichage ou traitement."""
        return {
            "type": self.get_type(),
            "message": self.get_message(),
            "date": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "data": self.get_data(),
            "actions": self.get_actions()
        }

    def get_data(self):
        """Retourne les données associées à l'alerte (identifiants étudiant et/ou cours)."""
        data = {}
        if self.student:
            data["student_id"] = self.student.id
        if self.course:
            data["course_id"] = self.course.id
        return data
