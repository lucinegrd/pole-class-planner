
from .registration_state_base import RegistrationState
from app.services.singletons.logger_singleton import Logger
from ..strategies.strategy_base import StudentStrategy
from ...repositories.registration_repository import RegistrationRepository


class AskedState(RegistrationState):
    def validate(self, registration):
        strategy = StudentStrategy().get_student_credit_strategy(registration.student)
        if strategy.can_validate(registration):
            strategy.apply(registration)
            Logger().log(f"Validation de l'inscription de {registration.student.name} au cours de {registration.course.course_type.name}")
            RegistrationRepository.update_state(registration, "Validé")
        else :
            Logger().log(f"{registration.student.name} s'est inscrit.e au cours {registration.course.course_type.name} mais n'a pas d'abonnement ni de crédit.")

    def complete(self, registration):
        print("❌ Cannot complete a non-validated reservation")

    def cancel(self, registration):
        Logger().log(f"Annulation de l'inscription de {registration.student.name} au cours de {registration.course.course_type.name}")
        RegistrationRepository.update_state(registration, "Annulé")
