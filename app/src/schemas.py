import uuid

from pydantic import BaseModel, EmailStr


class ConditionThresholds(BaseModel):
    # For now, we are only considering temperature
    temperature: float


class SubscriptionRequest(BaseModel):
    email: EmailStr
    city: str
    condition_thresholds: ConditionThresholds


class AlertResponse(BaseModel):
    id: uuid.UUID
    subscription_id: uuid.UUID
    condition_triggered: dict
    is_active: bool
