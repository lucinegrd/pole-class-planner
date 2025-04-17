from app.services.factory_alerts.alert_credit import CreditAlert
from app.services.factory_alerts.alert_subscription_limit import SubscriptionLimitAlert


class AlertFactory:
    @staticmethod
    def create_alert(alert_type, **kwargs):
        alert_classes = {
            "plus_de_credit": CreditAlert,
            "subscription_limit": SubscriptionLimitAlert,
            "subscription_expired": SubscriptionLimitAlert,
        }
        if alert_type not in alert_classes:
            raise ValueError(f"Type d'alerte inconnu : {alert_type}")

        return alert_classes[alert_type](**kwargs)
