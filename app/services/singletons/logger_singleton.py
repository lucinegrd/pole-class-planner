from datetime import datetime

class Logger:
    """Singleton pour enregistrer des logs d'événements."""

    _instance = None
    logs = []

    def __new__(cls):
        """Crée une instance unique de Logger."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls.logs = []
        return cls._instance

    def log(self, message):
        """Ajoute un message aux logs avec un horodatage."""
        self.logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        })

    def get_logs(self):
        """Retourne la liste des logs enregistrés."""
        return self.logs
