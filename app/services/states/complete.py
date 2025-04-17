from .registration_state_base import RegistrationState

class CompleteState(RegistrationState):
    def validate(self, registration):
        return

    def complete(self, registration):
        return

    def cancel(self, registration):
        return

