"""Abstract repository interface for the Achievement domain."""

from abc import abstractmethod
from typing import List, Optional

from src.models.achievement import Achievement, UserAchievement
from src.repositories.abstract.base_repository import AbstractBaseRepository


class AbstractAchievementRepository(AbstractBaseRepository):
    """Abstract contract for achievement data persistence operations."""

    @abstractmethod
    async def get_all(self) -> List[Achievement]:
        """Fetch all achievement definitions.

        Returns:
            List[Achievement]: List of all Achievement documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Achievement]:
        """Fetch an achievement by its slug.

        Args:
            slug (str): Machine-readable identifier.

        Returns:
            Optional[Achievement]: The matching Achievement, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user_achievements(self, user_id: str) -> List[UserAchievement]:
        """Fetch all achievements earned by a user.

        Args:
            user_id (str): The user's document ID.

        Returns:
            List[UserAchievement]: List of UserAchievement documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def has_achievement(self, user_id: str, achievement_id: str) -> bool:
        """Check whether a user has already earned a specific achievement.

        Args:
            user_id (str): The user's document ID.
            achievement_id (str): The Achievement's document ID.

        Returns:
            bool: True if the user has already earned the achievement.
        """
        raise NotImplementedError

    @abstractmethod
    async def award(self, user_achievement: UserAchievement) -> UserAchievement:
        """Persist a newly earned achievement for a user.

        Args:
            user_achievement (UserAchievement): The document to insert.

        Returns:
            UserAchievement: The persisted UserAchievement with its assigned ID.
        """
        raise NotImplementedError
