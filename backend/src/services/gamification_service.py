"""Gamification service: XP award, level-up logic, and streak management."""

from datetime import UTC, datetime
from typing import Dict, List

from src.models.user import User
from src.repositories.abstract.user_repository import AbstractUserRepository

XP_THRESHOLDS: List[int] = [
    0, 300, 900, 2100, 6500, 14000, 28000, 48000,
    64000, 85000, 110000, 140000, 165000, 195000, 230000,
    270000, 310000, 330000, 345000, 355000,
]

TITLES: Dict[int, str] = {
    1: "Apprentice",
    5: "Journeyman",
    10: "Adept",
    15: "Expert",
    20: "Master",
}


def calculate_level(xp: int) -> int:
    """Calculate the level for a given XP total using XP_THRESHOLDS.

    Args:
        xp (int): Total experience points accumulated.

    Returns:
        int: The current level (1–20) derived by counting passed thresholds.
    """
    passed_count = 0
    for threshold in XP_THRESHOLDS:
        if xp >= threshold:
            passed_count += 1
    return min(passed_count, 20)


def get_title_for_level(level: int) -> str:
    """Return the avatar title for a given level.

    Args:
        level (int): The user's current level (1–20).

    Returns:
        str: The title string corresponding to the highest title key <= level.
    """
    sorted_keys = sorted(TITLES.keys(), reverse=True)
    for key in sorted_keys:
        if key <= level:
            return TITLES[key]
    return TITLES[1]


class GamificationService:
    """Orchestrates XP awarding, level-up recalculation, and streak updates.

    Attributes:
        _user_repository (AbstractUserRepository): Repository for user data operations.
    """

    def __init__(self, user_repository: AbstractUserRepository) -> None:
        """Initialise the service with a user repository.

        Args:
            user_repository (AbstractUserRepository): An AbstractUserRepository implementation.
        """
        self._user_repository = user_repository

    async def award_xp(self, user: User, xp_amount: int) -> User:
        """Add XP to a user, recalculate their level and title, then save.

        Args:
            user (User): The current User document.
            xp_amount (int): Amount of XP to award.

        Returns:
            User: The updated User document after mutation and save.
        """
        user.xp += xp_amount
        new_level = calculate_level(user.xp)
        user.level = new_level
        user.avatar_title = get_title_for_level(new_level)
        return await self._user_repository.update(user)

    async def update_streak(self, user: User) -> User:
        """Increment or reset the user's daily activity streak, then save.

        Args:
            user (User): The current User document with last_activity_date.

        Returns:
            User: The User document with updated streak fields after save.
        """
        today = datetime.now(UTC).date()
        if user.last_activity_date is None:
            return await self._initialise_streak(user, today)
        last_date = user.last_activity_date.date()
        days_passed = (today - last_date).days
        if days_passed == 0:
            return user
        if days_passed == 1:
            user.current_streak += 1
        else:
            user.current_streak = 1
        if user.current_streak > user.longest_streak:
            user.longest_streak = user.current_streak
        user.last_activity_date = datetime.now(UTC)
        return await self._user_repository.update(user)

    async def _initialise_streak(self, user: User, today: object) -> User:
        """Set initial streak values for a user with no prior activity record.

        Args:
            user (User): The user document to initialise.
            today (object): Today's date object (unused directly, sets datetime).

        Returns:
            User: The initialised and saved user document.
        """
        user.current_streak = 1
        user.longest_streak = 1
        user.last_activity_date = datetime.now(UTC)
        return await self._user_repository.update(user)
