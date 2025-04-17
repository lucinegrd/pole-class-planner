from app.services.singletons.alert_manager_singleton import AlertManager
from app.services.factory_alerts.factory_alert import AlertFactory
from app.services.strategies.strategy_base import StudentStrategy


class CreditPackStrategy(StudentStrategy):
    def can_validate(self, registration):
        if registration.student.credit_balance >= registration.course.course_type.credit :
            return True
        else :
            alert = AlertFactory.create_alert("plus_de_credit", student=registration.student, course=registration.course)
            AlertManager().add_alert(**alert.to_dict())

    def apply(self, registration):
        registration.student.credit_balance -= registration.course.course_type.credit
        if registration.student.credit_balance < 0:
            alert = AlertFactory.create_alert("low_credit", student=registration.student)
            AlertManager().add_alert(**alert.to_dict())


