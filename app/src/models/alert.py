import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from src.database import Base


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subscriptions.id", ondelete="CASCADE"),
        nullable=False,
    )

    condition_triggered = Column(JSONB, nullable=False)
    triggered_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    subscription = relationship("Subscription", back_populates="alerts")
    is_active = Column(Boolean, default=False, nullable=False)
