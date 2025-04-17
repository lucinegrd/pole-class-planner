class StudentStrategy:
    """Classe de base pour définir une stratégie de validation d'inscription selon le type d'accès d'un étudiant."""

    def can_validate(self, registration) -> bool:
        """Vérifie si l'inscription peut être validée selon la stratégie."""
        raise NotImplementedError()

    def apply(self, registration):
        """Applique la validation (exemple : soustraire un crédit)."""
        raise NotImplementedError()

    @staticmethod
    def get_student_credit_strategy(student):
        """
        Retourne la stratégie adaptée à l'étudiant :
        - Abonnement actif → MonthlySubscriptionStrategy
        - Crédit disponible → CreditPackStrategy
        - Sinon → NoAccessStrategy
        """
        from .credit_pack_strategy import CreditPackStrategy
        from .no_access_strategy import NoAccessStrategy
        from .monthly_subscription_strategy import MonthlySubscriptionStrategy
        if hasattr(student, "subscriptions") and any(s.is_active_now() for s in student.subscriptions):
            return MonthlySubscriptionStrategy()
        elif student.credit_balance and student.credit_balance > 0:
            return CreditPackStrategy()
        else:
            return NoAccessStrategy()
