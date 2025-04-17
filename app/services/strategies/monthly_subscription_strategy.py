from app.services.singletons.alert_manager_singleton import AlertManager
from app.services.factory_alerts.factory_alert import AlertFactory
from app.services.strategies.strategy_base import StudentStrategy

class MonthlySubscriptionStrategy(StudentStrategy):
    """Stratégie de validation basée sur un abonnement mensuel."""

    def can_validate(self, registration):
        """Vérifie si l'étudiant peut valider son inscription en fonction de sa limite hebdomadaire d'abonnement."""
        for sub in registration.student.subscriptions:
            if sub.is_active_on(registration.course.date):
                nb_validated = sum(
                    1 for r in registration.student.registrations
                    if r.state == "Validé"
                    and r.course.date.isocalendar()[1] == registration.course.date.isocalendar()[1]
                )
                if nb_validated < sub.weekly_limit:
                    return True
                else:
                    alert = AlertFactory.create_alert("subscription_limit", student=registration.student, course=registration.course)
                    AlertManager().add_alert(**alert.to_dict())
                    return False
        alert = AlertFactory.create_alert("subscription_limit", student=registration.student, course=registration.course)
        AlertManager().add_alert(**alert.to_dict())
        return False

    def apply(self, registration):
        """Ne fait rien : la validation par abonnement n'implique pas de soustraction de crédits."""
        pass
