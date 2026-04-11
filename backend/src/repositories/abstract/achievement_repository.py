"""Abstract repository interface for the Achievement domain."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.achievement import Achievement, UserAchievement


class AbstractAchievementRepository(ABC):
    """Abstract contract for achievement data persistence operations."""

    @abstractmethod
    async def get_all(self) -> List[Achievement]:
        """Fetch all achievement definitions.

        Returns:
            List of all Achievement documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Achievement]:
        """Fetch an achievement definition by its slug.

        Args:
            slug: Machine-readable identifier.

        Returns:
            The matching Achievement, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user_achievements(self, user_id: str) -> List[UserAchievement]:
        """Fetch all achievements earned by a user.

        Args:
            user_id: The user's document ID.

        Returns:
            List of UserAchievement documents for the given user.
        """
        raise NotImplementedError

    @abstractmethod
    async def has_achievement(self, user_id: str, achievement_id: str) -> bool:
        """Check whether a user has already earned a specific achievement.

        Args:
            user_id: The user's document ID.
            achievement_id: The Achievement's document ID.

        Returns:
            True if the user has already earned the achievement.
        """
        raise NotImplementedError

    @abstractmethod
    async def award(self, user_achievement: UserAchievement) -> UserAchievement:
        """Persist a newly earned achievement for a user.

        Args:
            user_achievement: The UserAchievement document to insert.

        Returns:
            The persisted UserAchievement with its assigned ID.
        """
        raise NotImplementedError
