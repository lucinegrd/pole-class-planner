from .registration_state_base import RegistrationState
from app.services.singletons.logger_singleton import Logger
from ...repositories.registration_repository import RegistrationRepository


class WaitingListState(RegistrationState):
    def validate(self, registration):
        if registration.course.places > 0 :
            RegistrationRepository.update_state(registration, "Non validé")
            RegistrationState.get_state_instance(registration).validate(registration)

    def complete(self, registration):
        print("❌ Cannot complete a non-validated reservation")

    def cancel(self, registration):
        Logger().log(f"Annulation de l'inscription de {registration.student.name} au cours de {registration.course.course_type.name}")
        RegistrationRepository.update_state(registration, "Annulé")
