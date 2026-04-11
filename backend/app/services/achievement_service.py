"""Achievement service: trigger checking and badge awarding."""

from typing import List

from app.models.achievement import Achievement, UserAchievement
from app.repositories.abstract.achievement_repository import AbstractAchievementRepository
from app.schemas.achievement import AchievementResponse, UserAchievementResponse


class AchievementService:
    """Handles achievement trigger evaluation and award persistence.

    Attributes:
        _achievement_repository: Injected repository for achievement operations.
    """

    def __init__(self, achievement_repository: AbstractAchievementRepository) -> None:
        """Initialise the service with an achievement repository.

        Args:
            achievement_repository: An AbstractAchievementRepository implementation.
        """
        self._achievement_repository = achievement_repository

    async def list_all(self) -> List[AchievementResponse]:
        """Return all achievement definitions.

        Returns:
            List of AchievementResponse objects.
        """
        achievements: List[Achievement] = await self._achievement_repository.get_all()
        return [
            AchievementResponse(
                id=str(a.id),
                slug=a.slug,
                title=a.title,
                description=a.description,
                icon=a.icon,
                xp_reward=a.xp_reward,
            )
            for a in achievements
        ]

    async def list_user_achievements(self, user_id: str) -> List[UserAchievementResponse]:
        """Return achievements earned by a specific user.

        Args:
            user_id: The user's document ID.

        Returns:
            List of UserAchievementResponse objects.
        """
        # TODO: join with Achievement definitions for full data
        raise NotImplementedError

    async def check_and_award(
        self, user_id: str, trigger_type: str, current_value: int
    ) -> List[str]:
        """Evaluate all achievements matching a trigger type and award eligible ones.

        Args:
            user_id: The user's document ID.
            trigger_type: The type of event that triggered this check.
            current_value: The current value to compare against trigger thresholds.

        Returns:
            List of achievement slugs newly awarded in this call.
        """
        all_achievements: List[Achievement] = await self._achievement_repository.get_all()
        newly_awarded: List[str] = []

        for achievement in all_achievements:
            if achievement.trigger_type != trigger_type:
                continue
            if current_value < achievement.trigger_value:
                continue
            already_has = await self._achievement_repository.has_achievement(
                user_id=user_id, achievement_id=str(achievement.id)
            )
            if already_has is True:
                continue
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=str(achievement.id),
            )
            await self._achievement_repository.award(user_achievement)
            newly_awarded.append(achievement.slug)

        return newly_awarded
