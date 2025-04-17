from .registration_state_base import RegistrationState

class CompleteState(RegistrationState):
    """État d'une inscription confirmée (élève présent au cours)."""

    def validate(self, registration):
        """Impossible de valider une inscription déjà confirmée."""
        return

    def complete(self, registration):
        """L'inscription est déjà confirmée."""
        return

    def cancel(self, registration):
        """Impossible d'annuler une inscription déjà confirmée."""
        return
