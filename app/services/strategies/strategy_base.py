class StudentStrategy:
    def can_validate(self, registration) -> bool:
        raise NotImplementedError()

    def apply(self, registration):
        """Applique la validation : ex. soustraire un crédit"""
        raise NotImplementedError()

    @staticmethod
    def get_student_credit_strategy(student):
        from .credit_pack_strategy import CreditPackStrategy
        from .no_access_strategy import NoAccessStrategy
        from .monthly_subscription_strategy import MonthlySubscriptionStrategy
        if hasattr(student, "subscriptions") and any(s.is_active_now() for s in student.subscriptions):
            return MonthlySubscriptionStrategy()
        elif student.credit_balance and student.credit_balance > 0:
            return CreditPackStrategy()
        else:
            return NoAccessStrategy()

