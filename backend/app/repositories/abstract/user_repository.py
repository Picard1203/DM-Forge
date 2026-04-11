"""Abstract repository interface for the User domain."""

from abc import ABC, abstractmethod
from typing import Optional

from app.models.user import User


class AbstractUserRepository(ABC):
    """Abstract contract for user data persistence operations.

    All methods are async to support non-blocking I/O in FastAPI.
    Concrete implementations are located in repositories/mongodb/.
    """

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Fetch a user by their MongoDB document ID.

        Args:
            user_id: String representation of the MongoDB ObjectId.

        Returns:
            The matching User document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by their email address.

        Args:
            email: The email address to search for.

        Returns:
            The matching User document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Fetch a user by their username.

        Args:
            username: The username to search for.

        Returns:
            The matching User document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, user: User) -> User:
        """Persist a new user document.

        Args:
            user: The User instance to insert.

        Returns:
            The persisted User document with its assigned ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User) -> User:
        """Persist changes to an existing user document.

        Args:
            user: The User instance with updated fields.

        Returns:
            The updated User document.
        """
        raise NotImplementedError
