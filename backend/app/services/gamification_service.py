"""Gamification service: XP award, level-up logic, and streak management."""

from datetime import datetime, timedelta
from typing import Optional

from app.models.user import User
from app.repositories.abstract.user_repository import AbstractUserRepository
from app.services.achievement_service import AchievementService
from app.services.user_service import calculate_level, get_title_for_level


class GamificationService:
    """Orchestrates XP awarding, levelling, and streak updates.

    Attributes:
        _user_repository: Injected repository for user data operations.
        _achievement_service: Injected service for achievement checks.
    """

    def __init__(
        self,
        user_repository: AbstractUserRepository,
        achievement_service: AchievementService,
    ) -> None:
        """Initialise the service with a user repository and achievement service.

        Args:
            user_repository: An AbstractUserRepository implementation.
            achievement_service: An AchievementService instance.
        """
        self._user_repository = user_repository
        self._achievement_service = achievement_service

    async def award_xp_and_check(self, user: User, xp_amount: int) -> User:
        """Add XP, recalculate level/title, update streak, check achievements.

        Args:
            user: The current User document.
            xp_amount: Amount of XP to award.

        Returns:
            The updated User document after all mutations are persisted.
        """
        if xp_amount <= 0:
            return user

        user.xp += xp_amount
        new_level = calculate_level(user.xp)
        user.level = new_level
        user.avatar_title = get_title_for_level(new_level)
        user = await self._update_streak(user)
        updated_user = await self._user_repository.update(user)

        await self._achievement_service.check_and_award(
            user_id=str(updated_user.id),
            trigger_type="xp_total",
            current_value=updated_user.xp,
        )
        await self._achievement_service.check_and_award(
            user_id=str(updated_user.id),
            trigger_type="level",
            current_value=updated_user.level,
        )
        await self._achievement_service.check_and_award(
            user_id=str(updated_user.id),
            trigger_type="streak",
            current_value=updated_user.current_streak,
        )

        return updated_user

    async def _update_streak(self, user: User) -> User:
        """Increment or reset the user's daily activity streak.

        Args:
            user: The current User document with ``last_activity_date``.

        Returns:
            The User document with updated streak fields (not yet persisted).
        """
        now = datetime.utcnow()
        today = now.date()

        if user.last_activity_date is None:
            user.current_streak = 1
            user.longest_streak = 1
            user.last_activity_date = now
            return user

        last_date = user.last_activity_date.date()
        delta = today - last_date

        if delta == timedelta(days=0):
            return user

        if delta == timedelta(days=1):
            user.current_streak += 1
        else:
            user.current_streak = 1

        if user.current_streak > user.longest_streak:
            user.longest_streak = user.current_streak

        user.last_activity_date = now
        return user
