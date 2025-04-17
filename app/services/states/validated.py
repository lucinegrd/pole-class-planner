from .registration_state_base import RegistrationState
from app.services.singletons.logger_singleton import Logger
from ...repositories.registration_repository import RegistrationRepository


class ValidatedState(RegistrationState):
    def validate(self, registration):
        return

    def complete(self, registration):
        RegistrationRepository.update_state(registration, "Confirmé")

    def cancel(self, registration):
        Logger().log(f"Annulation de l'inscription de {registration.student.name} au cours de {registration.course.course_type.name}")
        RegistrationRepository.update_state(registration, "Annulé")
