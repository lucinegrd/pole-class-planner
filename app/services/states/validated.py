from .registration_state_base import RegistrationState
from app.services.singletons.logger_singleton import Logger
from ...repositories.registration_repository import RegistrationRepository

class ValidatedState(RegistrationState):
    """État d'une inscription validée mais pas encore confirmée."""

    def validate(self, registration):
        """L'inscription est déjà validée."""
        return

    def complete(self, registration):
        """Confirme une inscription validée."""
        RegistrationRepository.update_state(registration, "Confirmé")

    def cancel(self, registration):
        """Annule une inscription validée."""
        Logger().log(f"Annulation de l'inscription de {registration.student.name} au cours de {registration.course.course_type.name}")
        RegistrationRepository.update_state(registration, "Annulé")
