from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.celery_tasks.tasks import send_subscription_email
from src.models.alert import Alert
from src.models.subscription import Subscription
from src.schemas import SubscriptionRequest


def user_subscribe(db: Session, subscription: SubscriptionRequest):
    """
    Register a new user subscription.

    - db (Session): Database session.
    - subscription (SubscriptionRequest): Subscription details, including email and city.

    Raises:
    - `HTTPException (400)`: If the email is already registered.

    Process:
    1. Check if the email is already subscribed.
    2. If not, create a new subscription record.
    3. Commit the subscription to the database.
    4. Send a confirmation email asynchronously.

    Returns:
    - `Subscription`: The newly created subscription object.
    """
    existing_subscription = get_subscripter_by_email(db, subscription.email)
    if existing_subscription:
        raise HTTPException(
            status_code=400, detail="Email is already registered for a subscription."
        )
    new_subscription = Subscription(**subscription.model_dump())
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    send_subscription_email.delay(new_subscription.email, new_subscription.city)
    return new_subscription


def get_subscripter_by_email(db: Session, email: str) -> Subscription | None:
    """
    Retrieve a subscriber by email.

    - db (Session): Database session.
    - email (str): Email address to look up.

    Returns:
    - `Subscription | None`: Subscription object if found, otherwise `None`.
    """
    return db.query(Subscription).filter(Subscription.email == email).first()


def get_active_alerts(db: Session) -> list[Alert]:
    """
    Retrieve all active alerts.

    - db (Session): Database session.

    Returns:
    - `list[Alert]`: A list of active alerts.
    """
    return db.query(Alert).filter(Alert.is_active == True).all()
