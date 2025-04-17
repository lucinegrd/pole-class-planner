from app.services.factory_alerts.alert import Alert

class SubscriptionLimitAlert(Alert):
    """Alerte lorsqu'un étudiant dépasse sa limite hebdomadaire d'abonnement."""

    def get_type(self):
        """Retourne le type de l'alerte : 'subscription_limit'."""
        return "subscription_limit"

    def get_message(self):
        """Retourne le message associé à une limite hebdomadaire dépassée."""
        return f"{self.student.name} a dépassé sa limite hebdo d'abonnement pour le cours du {self.course.date.strftime('%d/%m')}"

    def get_actions(self):
        """Retourne les actions possibles pour une alerte de limite d'abonnement."""
        return ["valider_quand_meme", "annuler_reservation"]
