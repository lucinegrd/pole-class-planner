from app.services.factory_alerts.alert import Alert


class CreditAlert(Alert):
    def get_type(self):
        return "plus_de_credit"

    def get_message(self):
        return f"{self.student.name} n’a pas assez de crédits pour le cours du {self.course.date.strftime('%d/%m')}"

    def get_actions(self):
        return ["valider_quand_meme", "annuler_reservation"]
