from .registration_state_base import RegistrationState

class CanceledState(RegistrationState):
    """État d'une inscription annulée."""

    def validate(self, registration):
        """Impossible de valider une inscription annulée."""
        return

    def complete(self, registration):
        """Impossible de confirmer une inscription annulée."""
        return

    def cancel(self, registration):
        """L'inscription est déjà annulée"""
        return
