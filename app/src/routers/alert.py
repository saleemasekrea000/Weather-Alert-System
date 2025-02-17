from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.schemas import AlertResponse, SubscriptionRequest
from src.services import alert as alert_service

alert_router = APIRouter(prefix="/alert", tags=["alert"])


@alert_router.post(
    "/subscribe",
    summary="Subscribe to Alerts",
    description="Allows a user to subscribe to alerts by providing subscription details.",
    response_model=SubscriptionRequest,
)
def subscribe(
    subscription: SubscriptionRequest, db: Session = Depends(get_db)
) -> SubscriptionRequest:
    """
    - subscription: Subscription details (request body).
    - db: Database session (dependency).
    """
    return alert_service.user_subscribe(db, subscription)


@alert_router.get(
    "/active",
    summary="Get Active Alerts",
    description="Retrieves a list of currently active alerts.",
    response_model=list[AlertResponse],
)
def active_alerts(db: Session = Depends(get_db)) -> list[AlertResponse]:

    """
    - **db**: Database session (dependency).
    """
    return alert_service.get_active_alerts(db)
