"""
Represents user accounts with authentication and subscription information.
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
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from src.database.models.base_model import Base


class User(Base):
    """
    Stores user credentials, plan subscriptions, and account status.
    Includes tracking for total token usage and email verification.

    Attributes:
        id: Unique user identifier
        username: Unique username for login
        email: User's email address (unique)
        hashed_password: Securely hashed password
        plan_id: Reference to user's current subscription plan
        total_tokens_used: Lifetime token consumption
        is_active: Whether the account is active
        email_verified: Email verification status
        last_login_at: Timestamp of last successful login
        created_at: Account creation time
        updated_at: Last account modification

    Relationships:
        plan: The user's subscription plan
        chat_sessions: All chat sessions created by this user
        documents: All documents uploaded by this user
        chat_messages: All messages sent by this user
        usage_stats: Daily usage statistics for this user
    """

    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plan.id"), nullable=False)
    total_tokens_used = Column(BigInteger, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    email_verified = Column(Boolean, nullable=False, default=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    plan = relationship("Plan", back_populates="users")
    chat_sessions = relationship(
        "ChatSession", back_populates="user", cascade="all, delete-orphan"
    )
    """documents = relationship(
        "Document", back_populates="user", cascade="all, delete-orphan"
    )
    chat_messages = relationship("ChatMessage", back_populates="user")
    usage_stats = relationship(
        "UsageStats", back_populates="user", cascade="all, delete-orphan"
    )"""

    # Validation
    @validates("email")
    def validate_email(self, key, email):
        """Basic email validation"""
        if "@" not in email or "." not in email.split("@")[1]:
            raise ValueError("Invalid email format")
        return email.lower()

    @validates("total_tokens_used")
    def validate_tokens(self, key, tokens):
        """Ensure token count is non-negative"""
        if tokens < 0:
            raise ValueError("Token count cannot be negative")
        return tokens

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
