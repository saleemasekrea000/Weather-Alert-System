from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas import SubscriptionRequest
from src.services import alert as alert_service
from src.dependencies import get_db
from src.schemas import AlertResponse
alert_router = APIRouter(prefix="/alert", tags=["alert"])


@alert_router.post("/subscribe")
def subscribe(
    subscription: SubscriptionRequest, db: Session = Depends(get_db)
) -> SubscriptionRequest:
    return alert_service.user_subscribe(db, subscription)

@alert_router.get("/active")
def active_alerts(db: Session = Depends(get_db)) -> list[AlertResponse]:
    return alert_service.get_active_alerts(db)