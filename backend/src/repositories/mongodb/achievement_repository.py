"""MongoDB implementation of the AbstractAchievementRepository."""

from typing import List, Optional

from src.models.achievement import Achievement, UserAchievement
from src.repositories.abstract.achievement_repository import AbstractAchievementRepository


class MongoAchievementRepository(AbstractAchievementRepository):
    """Concrete MongoDB repository for Achievement documents using Beanie ODM."""

    async def get_all(self) -> List[Achievement]:
        """Fetch all achievement definitions.

        Returns:
            List of all Achievement documents.
        """
        return await Achievement.find_all().to_list()

    async def get_by_slug(self, slug: str) -> Optional[Achievement]:
        """Fetch an achievement by its slug.

        Args:
            slug: Machine-readable identifier.

        Returns:
            The matching Achievement, or None if not found.
        """
        return await Achievement.find_one(Achievement.slug == slug)

    async def get_user_achievements(self, user_id: str) -> List[UserAchievement]:
        """Fetch all achievements earned by a user.

        Args:
            user_id: The user's document ID.

        Returns:
            List of UserAchievement documents for the given user.
        """
        return await UserAchievement.find(UserAchievement.user_id == user_id).to_list()

    async def has_achievement(self, user_id: str, achievement_id: str) -> bool:
        """Check whether a user has already earned a specific achievement.

        Args:
            user_id: The user's document ID.
            achievement_id: The Achievement's document ID.

        Returns:
            True if the user has already earned the achievement.
        """
        existing = await UserAchievement.find_one(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == achievement_id,
        )
        return existing is not None

    async def award(self, user_achievement: UserAchievement) -> UserAchievement:
        """Persist a newly earned achievement for a user.

        Args:
            user_achievement: The UserAchievement document to insert.

        Returns:
            The persisted UserAchievement with its assigned ID.
        """
        await user_achievement.insert()
        return user_achievement
