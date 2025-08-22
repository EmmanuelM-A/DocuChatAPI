"""
Represents subscription plans that define user limits and pricing.
"""

import uuid
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    BigInteger,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    DECIMAL,
    JSON,
    Index,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.models.base import Base


class Plan(Base):
    """
    This model stores different subscription tiers (free, pro, enterprise)
    with their associated limits for tokens, documents, and sessions.

    Attributes:
        id: Unique plan identifier
        name: Plan name (e.g., 'free', 'pro', 'enterprise')
        token_limit_daily: Daily token allowance for this plan
        document_limit: Maximum documents per session
        session_limit: Maximum concurrent sessions
        price_monthly: Monthly cost in USD
        is_active: Whether this plan is available for new subscriptions
        created_at: Plan creation timestamp

    Relationships:
        users: List of users subscribed to this plan
    """

    __tablename__ = "plan"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)
    token_limit_daily = Column(Integer, nullable=False)
    document_limit = Column(Integer, nullable=False)
    session_limit = Column(Integer, nullable=False)
    price_monthly = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    users = relationship("User", back_populates="plan")

    # Constraints
    __table_args__ = (
        CheckConstraint("token_limit_daily >= 0", name="check_positive_token_limit"),
        CheckConstraint("document_limit >= 0", name="check_positive_document_limit"),
        CheckConstraint("session_limit >= 0", name="check_positive_session_limit"),
        CheckConstraint("price_monthly >= 0", name="check_positive_price"),
    )

    def __repr__(self):
        return f"<Plan(name='{self.name}', price=${self.price_monthly}/mo)>"
