"""
User Schema
"""

from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str
    email: str
    hashed_password: str
    plan: str = "free"
    total_tokens_used: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
