"""
This module provides the repository class for interacting with the `User`
model.
"""

from typing import Any, Dict, List, Optional, Sequence, Tuple
from uuid import UUID

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.user_model import User


class UserRepository:
    """
    Repository for performing database operations on the User model.

    Responsibilities:
        - Encapsulate queries/mutations for the `user` table.
        - Provide reusable methods for services and APIs.
        - Ensure consistent access patterns for the User entity.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user_data: Dict[str, Any]) -> User:
        """Create and persist a new user."""
        user = User(**user_data)
        self.db.add(user)
        await self.db.flush()  # Persist without committing yet
        return user

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Retrieve a user by primary key."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, user_email: str) -> Optional[User]:
        """Retrieve a user by email address."""
        result = await self.db.execute(select(User).where(User.email == user_email))
        return result.scalars().first()

    async def get_by_criteria(self, criteria: Dict[str, Any]) -> Optional[User]:
        """Retrieve the first user matching given criteria."""
        stmt = select(User)
        for field, value in criteria.items():
            stmt = stmt.where(getattr(User, field) == value)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update(self, user_id: UUID, data: Dict[str, Any]) -> Optional[User]:
        """Update fields on a user and return the updated instance."""
        stmt = update(User).where(User.id == user_id).values(**data).returning(User)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def delete(self, user_id: UUID) -> None:
        """Delete a user by ID."""
        await self.db.execute(delete(User).where(User.id == user_id))

    async def get_all_by_criteria(self, criteria: Dict[str, Any]) -> List[User]:
        """Retrieve all users matching given criteria."""
        stmt = select(User)
        for field, value in criteria.items():
            stmt = stmt.where(getattr(User, field) == value)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def exists(self, user_id: UUID) -> Optional[User]:
        """
        Check whether a user exists with the given ID.

        Args:
            user_id (UUID): The user's identifier (primary key).

        Returns:
            bool: True if the user exists, False otherwise.
        """
        stmt = select(1).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.first() is not None

    async def count(self, criteria: Dict[str, Any]) -> int:
        """Count number of users matching criteria."""
        stmt = select(func.count()).select_from(User)
        for field, value in criteria.items():
            stmt = stmt.where(getattr(User, field) == value)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def create_many(self, users: Sequence[Dict[str, Any]]) -> List[User]:
        """Bulk insert multiple users."""
        user_objs = [User(**data) for data in users]
        self.db.add_all(user_objs)
        await self.db.flush()
        return user_objs

    async def delete_many(self, user_ids: Sequence[UUID]) -> None:
        """Delete multiple users by IDs."""
        await self.db.execute(delete(User).where(User.id.in_(user_ids)))

    async def get_with_pagination(
        self, page: int, limit: int, criteria: Dict[str, Any]
    ) -> Tuple[List[User], int]:
        """
        Retrieve users with pagination.

        Returns:
            (list_of_users, total_count).
        """
        stmt = select(User)
        for field, value in criteria.items():
            stmt = stmt.where(getattr(User, field) == value)

        total_result = await self.db.execute(
            select(func.count()).select_from(User).filter(*stmt._where_criteria)
        )
        total = total_result.scalar_one()

        result = await self.db.execute(stmt.offset((page - 1) * limit).limit(limit))
        users = result.scalars().all()
        return users, total
