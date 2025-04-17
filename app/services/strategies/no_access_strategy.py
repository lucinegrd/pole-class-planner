from app.services.singletons.alert_manager_singleton import AlertManager
from app.services.factory_alerts.factory_alert import AlertFactory
from app.services.strategies.strategy_base import StudentStrategy


class NoAccessStrategy(StudentStrategy):
    def can_validate(self, registration):
        alert = AlertFactory.create_alert("plus_de_credit", student=registration.student, course=registration.course)
        AlertManager().add_alert(**alert.to_dict())
        return False

    def apply(self, registration):
        pass
