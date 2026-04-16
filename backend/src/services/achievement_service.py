"""Achievement service: trigger checking and badge awarding."""

from typing import List, Optional

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
            responses.append(self._to_response(achievement))
        return responses

    async def list_user_achievements(self, user_id: str) -> List[UserAchievementResponse]:
        """Return achievements earned by a specific user, joined with their definitions.

        Args:
            user_id (str): The user's document ID.

        Returns:
            List[UserAchievementResponse]: Resolved achievement records with earned_at.
        """
        user_achievements = await self._achievement_repository.get_user_achievements(
            user_id=user_id
        )
        all_achievements = await self._achievement_repository.get_all()
        achievement_map: dict = {}
        for item in all_achievements:
            achievement_map[str(item.id)] = item
        responses: List[UserAchievementResponse] = []
        for user_achievement in user_achievements:
            matched: Optional[Achievement] = achievement_map.get(user_achievement.achievement_id)
            if matched is not None:
                responses.append(
                    UserAchievementResponse(
                        id=str(matched.id),
                        slug=matched.slug,
                        title=matched.title,
                        description=matched.description,
                        icon=matched.icon,
                        xp_reward=matched.xp_reward,
                        earned_at=user_achievement.earned_at,
                    )
                )
        return responses

    async def check_and_award(
        self, user_id: str, event_type: str, event_value: str
    ) -> List[AchievementResponse]:
        """Evaluate all achievements matching a trigger type and award eligible ones.

        Args:
            user_id (str): The user's document ID.
            event_type (str): The type of event that triggered this check.
            event_value (str): The value to compare against each achievement's trigger_value.

        Returns:
            List[AchievementResponse]: Achievements newly awarded in this call.
        """
        all_achievements: List[Achievement] = await self._achievement_repository.get_all()
        newly_awarded: List[AchievementResponse] = []
        for achievement in all_achievements:
            is_matching_type = achievement.trigger_type == event_type
            is_matching_value = self._matches_trigger(
                achievement=achievement, event_value=event_value
            )
            if is_matching_type is True and is_matching_value is True:
                already_has = await self._achievement_repository.has_achievement(
                    user_id=user_id, achievement_id=str(achievement.id)
                )
                if already_has is False:
                    user_achievement = UserAchievement(
                        user_id=user_id,
                        achievement_id=str(achievement.id),
                    )
                    await self._achievement_repository.award(user_achievement)
                    newly_awarded.append(self._to_response(achievement))
        return newly_awarded

    def _matches_trigger(self, achievement: Achievement, event_value: str) -> bool:
        """Check whether an event value satisfies an achievement's trigger condition.

        Numeric trigger_values (e.g. "10", "50") use a <= comparison against the event
        value converted to int. The special value "any" always matches. The special value
        "all" matches only when event_value is also "all". Otherwise an exact string match
        is used (for module slug triggers).

        Args:
            achievement (Achievement): The achievement to evaluate.
            event_value (str): The value produced by the triggering event.

        Returns:
            bool: True if the event_value satisfies the trigger condition.
        """
        trigger = achievement.trigger_value
        if trigger == "any":
            return True
        if trigger == "all":
            return event_value == "all"
        try:
            return int(trigger) <= int(event_value)
        except ValueError:
            return trigger == event_value

    def _to_response(self, achievement: Achievement) -> AchievementResponse:
        """Serialise an Achievement document to an AchievementResponse.

        Args:
            achievement (Achievement): The Achievement document.

        Returns:
            AchievementResponse: Serialised response object.
        """
        return AchievementResponse(
            id=str(achievement.id),
            slug=achievement.slug,
            title=achievement.title,
            description=achievement.description,
            icon=achievement.icon,
            xp_reward=achievement.xp_reward,
        )
