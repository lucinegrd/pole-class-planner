from app.services.factory_alerts.alert import Alert

class CreditAlert(Alert):
    """Alerte pour un manque de crédits d'un étudiant."""

    def get_type(self):
        """Retourne le type de l'alerte : 'plus_de_credit'."""
        return "plus_de_credit"

    def get_message(self):
        """Retourne le message associé à l'alerte de crédits insuffisants."""
        return f"{self.student.name} n’a pas assez de crédits pour le cours du {self.course.date.strftime('%d/%m')}"

    def get_actions(self):
        """Retourne les actions possibles pour une alerte de crédits."""
        return ["valider_quand_meme", "annuler_reservation"]
