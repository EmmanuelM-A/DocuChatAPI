"""
Responsible for communicating and accessing the user table in the database.
"""

from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    """
    Handles all queries and mutations against the user model.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: object):
        pass

    async def get_by_id(self, user_id: str):
        pass

    async def get_by_email(self, user_email: str):
        pass

    async def get_by_criteria(self, criteria: object):
        pass

    async def update(self, user_id: str, data):
        pass

    async def delete(self, user_id):
        pass

    async def get_all_by_criteria(self, criteria: object = {}):
        pass

    async def exists(self, criteria):
        pass

    async def count(self, criteria):
        pass

    async def create_many(self, users):
        pass

    async def delete_many(self, user_ids):
        pass

    async def get_as_pagination(self, page, limit, criteria):
        pass
