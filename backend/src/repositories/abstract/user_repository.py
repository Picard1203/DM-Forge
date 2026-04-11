"""Abstract repository interface for the User domain."""

from abc import abstractmethod
from typing import Optional

from src.models.user import User
from src.repositories.abstract.base_repository import AbstractBaseRepository


class AbstractUserRepository(AbstractBaseRepository):
    """Abstract contract for user data persistence operations."""

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Fetch a user by their MongoDB document ID.

        Args:
            user_id (str): String representation of the MongoDB ObjectId.

        Returns:
            Optional[User]: The matching User document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            Optional[User]: The matching User document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Fetch a user by their username.

        Args:
            username (str): The username to search for.

        Returns:
            Optional[User]: The matching User document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, user: User) -> User:
        """Persist a new user document.

        Args:
            user (User): The User instance to insert.

        Returns:
            User: The persisted User document with its assigned ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User) -> User:
        """Persist changes to an existing user document.

        Args:
            user (User): The User instance with updated fields.

        Returns:
            User: The updated User document.
        """
        raise NotImplementedError
