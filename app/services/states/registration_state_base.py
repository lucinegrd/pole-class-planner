class RegistrationState:
    """Classe de base pour représenter l'état d'une inscription."""

    def validate(self, registration):
        """Valide une inscription (méthode à implémenter dans les sous-classes)."""
        raise NotImplementedError()

    def complete(self, registration):
        """Marque une inscription comme confirmée (méthode à implémenter dans les sous-classes)."""
        raise NotImplementedError()

    def cancel(self, registration):
        """Annule une inscription (méthode à implémenter dans les sous-classes)."""
        raise NotImplementedError()

    @staticmethod
    def get_state_instance(registration):
        """ Retourne une instance de l'état correspondant à l'inscription.
        """
        from .asked import AskedState
        from .validated import ValidatedState
        from .complete import CompleteState
        from .canceled import CanceledState
        from .waiting_list import WaitingListState
        state_map = {
            "Non validé": AskedState(),
            "Validé": ValidatedState(),
            "Confirmé": CompleteState(),
            "Annulé": CanceledState(),
            "Sur liste d'attente": WaitingListState()
        }
        return state_map.get(registration.state)
