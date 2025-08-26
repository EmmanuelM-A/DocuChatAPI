"""
This module defines Pydantic schemas for validating user-related data in the
API layer. Schemas ensure that incoming requests are validated and outgoing
responses are serialized in a consistent, secure, and well-typed format.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterUser(BaseModel):
    """Schema for registering a new user."""

    username: str
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    """Schema for logging in a user."""

    email: EmailStr
    password: str


class UserResponseData(BaseModel):
    """Schema for returning user information to clients."""

    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    plan_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
