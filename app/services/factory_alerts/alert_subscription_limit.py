from app.services.factory_alerts.alert import Alert


class SubscriptionLimitAlert(Alert):
    def get_type(self):
        return "subscription_limit"

    def get_message(self):
        return f"{self.student.name} a dépassé sa limite hebdo d'abonnement pour le cours du {self.course.date.strftime('%d/%m')}"

    def get_actions(self):
        return ["valider_quand_meme", "annuler_reservation"]
