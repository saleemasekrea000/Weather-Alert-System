from sqlalchemy.orm import Session

from src.schemas import SubscriptionRequest
from src.services.alert import (
    get_active_alerts,
    get_subscripter_by_email,
    user_subscribe,
)


def test_user_subscribe(db_session: Session, subscription_data: dict):
    subscription_request = SubscriptionRequest(**subscription_data)
    subscription = user_subscribe(db_session, subscription_request)
    assert subscription.email == subscription_data["email"]
    assert subscription.city == subscription_data["city"]


def test_get_subscripter_by_email(db_session: Session, subscription_data: dict):
    subscription_request = SubscriptionRequest(**subscription_data)
    user_subscribe(db_session, subscription_request)
    subscription = get_subscripter_by_email(db_session, subscription_data["email"])
    assert subscription.email == subscription_data["email"]
    assert subscription.city == subscription_data["city"]


def test_get_active_alerts(db_session: Session, subscription_data: dict):
    subscription_request = SubscriptionRequest(**subscription_data)
    user_subscribe(db_session, subscription_request)
    alerts = get_active_alerts(db_session)
    # No alerts should be active
    assert len(alerts) == 0
