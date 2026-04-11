"""Gamification service: XP award, level-up logic, and streak management."""

from datetime import UTC, datetime

from src.models.user import User
from src.repositories.abstract.user_repository import AbstractUserRepository
from src.services.achievement_service import AchievementService
from src.services.user_service import calculate_level, get_title_for_level


class GamificationService:
    """Orchestrates XP awarding, levelling, and streak updates.

    Attributes:
        _user_repository (AbstractUserRepository): Repository for user data operations.
        _achievement_service (AchievementService): Service for achievement checks.
    """

    def __init__(
        self,
        user_repository: AbstractUserRepository,
        achievement_service: AchievementService,
    ) -> None:
        """Initialise the service with a user repository and achievement service.

        Args:
            user_repository (AbstractUserRepository): An AbstractUserRepository implementation.
            achievement_service (AchievementService): An AchievementService instance.
        """
        self._user_repository = user_repository
        self._achievement_service = achievement_service

    async def award_xp_and_check(self, user: User, xp_amount: int) -> User:
        """Add XP, recalculate level/title, update streak, check achievements.

        Args:
            user (User): The current User document.
            xp_amount (int): Amount of XP to award.

        Returns:
            User: The updated User document after all mutations are persisted.
        """
        if xp_amount <= 0:
            return user
        self._update_user_stats(user, xp_amount)
        user = await self._update_streak(user)
        updated_user = await self._user_repository.update(user)
        await self._trigger_achievement_checks(updated_user)
        return updated_user

    def _update_user_stats(self, user: User, xp_amount: int) -> None:
        """Update XP and derive the new level and title.

        Args:
            user (User): The user document to modify.
            xp_amount (int): Experience points to add.
        """
        user.xp += xp_amount
        new_level = calculate_level(user.xp)
        user.level = new_level
        user.avatar_title = get_title_for_level(new_level)

    async def _trigger_achievement_checks(self, user: User) -> None:
        """Orchestrate all achievement trigger checks for a user.

        Args:
            user (User): The persisted user document to evaluate.
        """
        milestones = [
            ("xp_total", user.xp),
            ("level", user.level),
            ("streak", user.current_streak),
        ]
        for trigger_type, value in milestones:
            await self._achievement_service.check_and_award(
                user_id=str(user.id),
                trigger_type=trigger_type,
                current_value=value,
            )

    async def _update_streak(self, user: User) -> User:
        """Increment or reset the user's daily activity streak.

        Args:
            user (User): The current User document with last_activity_date.

        Returns:
            User: The User document with updated streak fields.
        """
        now = datetime.now(UTC)
        if user.last_activity_date is None:
            return self._initialise_streak(user, now)
        days_passed = (now.date() - user.last_activity_date.date()).days
        if days_passed == 0:
            return user
        if days_passed == 1:
            user.current_streak += 1
        else:
            user.current_streak = 1
        if user.current_streak > user.longest_streak:
            user.longest_streak = user.current_streak
        user.last_activity_date = now
        return user

    def _initialise_streak(self, user: User, now: datetime) -> User:
        """Set initial streak values for a user with no previous activity.

        Args:
            user (User): The user to initialise.
            now (datetime): The current UTC timestamp.

        Returns:
            User: The initialised user document.
        """
        user.current_streak = 1
        user.longest_streak = 1
        user.last_activity_date = now
        return user
