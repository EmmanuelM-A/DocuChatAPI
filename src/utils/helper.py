"""
This module provides utility classes for common application-wide functionality.
"""

import bcrypt


class Cryptography:
    """Handles all operations that involved with cryptography"""

    @staticmethod
    async def hash_password(password: str) -> bytes:
        """
        Hashes a plain-text password using bcrypt with a generated salt.

        Args:
            password (str): The plain-text password to hash.

        Returns:
            bytes: The bcrypt hashed password, including the salt.
        """

        SALT_ROUNDS = 12
        salt = bcrypt.gensalt(SALT_ROUNDS)
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    @staticmethod
    async def verify_password(password: str, hashed_password: bytes) -> bool:
        """
        Verifies a plain-text password against its bcrypt hash.

        Args:
            password (str): The plain-text password to check.
            hashed_password (bytes): The bcrypt hashed password retrieved from storage.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """

        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


class Response:
    """
    Responsible for sending the http response objects to users using the standardized
    response format.
    """

    @staticmethod
    async def send_success_response():
        """Sets the status code and sends a standardized success response."""

    @staticmethod
    async def send_error_response():
        """Sets the status code and sends a standardized error response."""


class TokenUtil:
    """Handles all operations related to json web tokens."""

    @staticmethod
    async def generate_token(payload, jwt_secret, expiry):
        """Handles all operations related to json web tokens."""

    @staticmethod
    async def verify_token(token, jwt_secret):
        """Verifies the token using the JWT_SECRET."""
