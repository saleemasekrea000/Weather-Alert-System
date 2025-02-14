from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.schemas import SubscriptionRequest
from src.models.subscription import Subscription


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
    return new_subscription


def get_subscripter_by_email(db: Session, email: str):
    return db.query(Subscription).filter(Subscription.email == email).first()
