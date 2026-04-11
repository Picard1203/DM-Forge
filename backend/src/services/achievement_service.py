"""Achievement service: trigger checking and badge awarding."""

from typing import List

from src.models.achievement import Achievement, UserAchievement
from src.repositories.abstract.achievement_repository import AbstractAchievementRepository
from src.schemas.achievement import AchievementResponse, UserAchievementResponse


class AchievementService:
    """Handles achievement trigger evaluation and award persistence.

    Attributes:
        _achievement_repository (AbstractAchievementRepository): Injected repository.
    """

    def __init__(self, achievement_repository: AbstractAchievementRepository) -> None:
        """Initialise the service with an achievement repository.

        Args:
            achievement_repository (AbstractAchievementRepository): Repository instance.
        """
        self._achievement_repository = achievement_repository

    async def list_all(self) -> List[AchievementResponse]:
        """Return all achievement definitions.

        Returns:
            List[AchievementResponse]: List of AchievementResponse objects.
        """
        achievements: List[Achievement] = await self._achievement_repository.get_all()
        responses: List[AchievementResponse] = []
        for achievement in achievements:
            responses.append(
                AchievementResponse(
                    id=str(achievement.id),
                    slug=achievement.slug,
                    title=achievement.title,
                    description=achievement.description,
                    icon=achievement.icon_slug,
                    xp_reward=0,  # Placeholder until xp_reward added to model
                )
            )
        return responses

    async def list_user_achievements(self, user_id: str) -> List[UserAchievementResponse]:
        """Return achievements earned by a specific user.

        Args:
            user_id (str): The user's document ID.

        Returns:
            List[UserAchievementResponse]: List of UserAchievementResponse objects.
        """
        # TODO: join with Achievement definitions for full data
        raise NotImplementedError

    async def check_and_award(
        self, user_id: str, trigger_type: str, current_value: int
    ) -> List[str]:
        """Evaluate all achievements matching a trigger type and award eligible ones.

        Args:
            user_id (str): The user's document ID.
            trigger_type (str): The type of event that triggered this check.
            current_value (int): The value to compare against thresholds.

        Returns:
            List[str]: List of achievement slugs newly awarded in this call.
        """
        all_achievements: List[Achievement] = await self._achievement_repository.get_all()
        newly_awarded: List[str] = []
        for achievement in all_achievements:
            if (achievement.trigger_type == trigger_type) and (current_value >= achievement.trigger_threshold):
                already_has = await self._achievement_repository.has_achievement(
                    user_id=user_id, achievement_id=str(achievement.id)
                )
                if already_has is False:
                    user_achievement = UserAchievement(
                        user_id=user_id,
                        achievement_id=str(achievement.id),
                    )
                    await self._achievement_repository.award(user_achievement)
                    newly_awarded.append(achievement.slug)
        return newly_awarded
