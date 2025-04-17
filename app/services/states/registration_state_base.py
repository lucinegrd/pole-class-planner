
class RegistrationState:
    def validate(self, registration):
        raise NotImplementedError()

    def complete(self, registration):
        raise NotImplementedError()

    def cancel(self, registration):
        raise NotImplementedError()

    @staticmethod
    def get_state_instance(registration):
        # éviter les imports circulaires
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

