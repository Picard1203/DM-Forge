"""MongoDB implementation of the AbstractUserRepository."""

from typing import Optional

from beanie import PydanticObjectId

from src.models.user import User
from src.repositories.abstract.user_repository import AbstractUserRepository


class MongoUserRepository(AbstractUserRepository):
    """Concrete MongoDB repository for User documents using Beanie ODM."""

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Fetch a user by their MongoDB document ID.

        Args:
            user_id (str): String representation of the MongoDB ObjectId.

        Returns:
            Optional[User]: The matching User document, or None if not found.
        """
        return await User.get(PydanticObjectId(user_id))

    async def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            Optional[User]: The matching User document, or None if not found.
        """
        return await User.find_one(User.email == email)

    async def get_by_username(self, username: str) -> Optional[User]:
        """Fetch a user by their username.

        Args:
            username (str): The username to search for.

        Returns:
            Optional[User]: The matching User document, or None if not found.
        """
        return await User.find_one(User.username == username)

    async def create(self, user: User) -> User:
        """Persist a new user document.

        Args:
            user (User): The User instance to insert.

        Returns:
            User: The persisted User document with its assigned ID.
        """
        await user.insert()
        return user

    async def update(self, user: User) -> User:
        """Persist changes to an existing user document.

        Args:
            user (User): The User instance with updated fields.

        Returns:
            User: The updated User document.
        """
        await user.save()
        return user
