"""
Represents individual conversation sessions between users and the AI assistant.
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


class ChatSession(Base):
    """
    Each session represents a logical conversation thread that can contain
    multiple messages and associated documents. Sessions track metadata
    like total messages and token usage.

    Attributes:
        id: Unique session identifier
        user_id: Reference to the session owner
        title: User-defined or auto-generated session title
        description: Optional session description
        total_messages: Cached count of messages in this session
        total_tokens: Cached token usage for this session
        created_at: Session creation time
        updated_at: Last session modification

    Relationships:
        user: The user who owns this session
        documents: Documents uploaded to this session
        chat_messages: All messages in this conversation
    """

    __tablename__ = "chat_session"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    total_messages = Column(Integer, nullable=False, default=0)
    total_tokens = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    """documents = relationship(
        "Document", back_populates="session", cascade="all, delete-orphan"
    )
    chat_messages = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan"
    )"""

    # Constraints
    __table_args__ = (
        CheckConstraint("total_messages >= 0", name="check_positive_message_count"),
        CheckConstraint("total_tokens >= 0", name="check_positive_token_count"),
        Index("idx_session_user_created", "user_id", "created_at"),
    )

    def __repr__(self):
        return f"<ChatSession(title='{self.title}', messages={self.total_messages})>"
