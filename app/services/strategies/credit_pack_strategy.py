from app.services.singletons.alert_manager_singleton import AlertManager
from app.services.factory_alerts.factory_alert import AlertFactory
from app.services.strategies.strategy_base import StudentStrategy

class CreditPackStrategy(StudentStrategy):
    """Stratégie de validation basée sur l'utilisation de crédits."""

    def can_validate(self, registration):
        """Vérifie si l'étudiant a suffisamment de crédits pour valider l'inscription."""
        if registration.student.credit_balance >= registration.course.course_type.credit:
            return True
        else:
            alert = AlertFactory.create_alert("plus_de_credit", student=registration.student, course=registration.course)
            AlertManager().add_alert(**alert.to_dict())

    def apply(self, registration):
        """Soustrait les crédits nécessaires lors de la validation de l'inscription."""
        registration.student.credit_balance -= registration.course.course_type.credit
        if registration.student.credit_balance < 0:
            alert = AlertFactory.create_alert("low_credit", student=registration.student)
            AlertManager().add_alert(**alert.to_dict())
