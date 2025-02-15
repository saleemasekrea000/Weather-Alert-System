from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.celery_tasks.tasks import send_subscription_email
from src.models.alert import Alert
from src.models.subscription import Subscription
from src.schemas import SubscriptionRequest


def user_subscribe(db: Session, subscription: SubscriptionRequest):
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


def get_subscripter_by_email(db: Session, email: str):
    return db.query(Subscription).filter(Subscription.email == email).first()


def get_active_alerts(db: Session):
    return db.query(Alert).filter(Alert.is_active == True).all()
