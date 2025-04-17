class AlertManager:
    """Singleton pour gérer les alertes dans l'application."""

    _instance = None
    alerts = []

    def __new__(cls):
        """Crée une instance unique d'AlertManager."""
        if cls._instance is None:
            cls._instance = super(AlertManager, cls).__new__(cls)
            cls.alerts = []
        return cls._instance

    def add_alert(self, type, message, date, data, actions):
        """Ajoute une nouvelle alerte."""
        self.alerts.append({
            "id": len(self.alerts) + 1,
            "type": type,
            "message": message,
            "date": date,
            "data": data,
            "actions": actions
        })

    def get_alerts(self):
        """Retourne toutes les alertes, les plus récentes en premier."""
        return list(reversed(self.alerts))

    def get_alert_by_id(self, alert_id):
        """Récupère une alerte par son identifiant."""
        return next((a for a in self.alerts if a["id"] == alert_id), None)

    def remove_alert(self, alert_id):
        """Supprime une alerte par son identifiant."""
        self.alerts = [a for a in self.alerts if a["id"] != alert_id]

    def remove_alerts_by_type_and_student(self, alert_type, student_id):
        """Supprime toutes les alertes d'un type donné pour un étudiant donné."""
        self.alerts = [
            a for a in self.alerts
            if not (a["type"] == alert_type and a["data"].get("student_id") == student_id)
        ]
