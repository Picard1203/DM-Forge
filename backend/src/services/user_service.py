"""User service: profile management and XP/level calculations."""

from typing import Optional

from src.models.user import User, UserSettings
from src.repositories.abstract.user_repository import AbstractUserRepository
from src.schemas.user import UserUpdate
from src.utils.exceptions import UsernameAlreadyExistsError, UserNotFoundError

# XP thresholds per level (index = level - 1)
_LEVEL_THRESHOLDS = [0, 100, 250, 500, 900, 1400, 2000, 2700, 3500, 4500]
_TITLES = [
    "Apprentice",
    "Initiate",
    "Adventurer",
    "Hero",
    "Champion",
    "Veteran",
    "Master",
    "Grandmaster",
    "Legend",
    "Archon",
]


def calculate_level(xp: int) -> int:
    """Calculate the level for a given XP total.

    Args:
        xp: Total experience points.

    Returns:
        The level (1-indexed) corresponding to the XP total.
    """
    level = 1
    for threshold in _LEVEL_THRESHOLDS:
        if xp >= threshold:
            level += 1
    return min(level, len(_LEVEL_THRESHOLDS))


def get_title_for_level(level: int) -> str:
    """Return the avatar title for a given level.

    Args:
        level: The user's current level (1-indexed).

    Returns:
        The title string associated with the level.
    """
    index = min(level - 1, len(_TITLES) - 1)
    return _TITLES[index]


class UserService:
    """Handles user profile operations and gamification calculations.

    Attributes:
        _user_repository: Injected repository for user data operations.
    """

    def __init__(self, user_repository: AbstractUserRepository) -> None:
        """Initialise the service with a user repository.

        Args:
            user_repository: An AbstractUserRepository implementation.
        """
        self._user_repository = user_repository

    async def get_by_id(self, user_id: str) -> User:
        """Fetch a user by ID, raising if not found.

        Args:
            user_id: The user's document ID.

        Returns:
            The matching User document.

        Raises:
            UserNotFoundError: If no user with that ID exists.
        """
        user: Optional[User] = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        return user

    async def update_profile(self, user: User, update: UserUpdate) -> User:
        """Apply a partial profile update to a user.

        Args:
            user: The current User document.
            update: Validated update payload.

        Returns:
            The updated User document.

        Raises:
            UsernameAlreadyExistsError: If the new username is already taken.
        """
        if update.username is not None:
            existing: Optional[User] = await self._user_repository.get_by_username(
                update.username
            )
            if existing is not None and str(existing.id) != str(user.id):
                raise UsernameAlreadyExistsError()
            user.username = update.username

        if update.settings is not None:
            if update.settings.rotation_interval_minutes is not None:
                user.settings.rotation_interval_minutes = (
                    update.settings.rotation_interval_minutes
                )

        return await self._user_repository.update(user)

    async def award_xp(self, user: User, xp_amount: int) -> User:
        """Add XP to a user and recalculate their level and title.

        Args:
            user: The current User document.
            xp_amount: Amount of XP to add.

        Returns:
            The updated User document with new XP, level, and title.
        """
        user.xp += xp_amount
        new_level = calculate_level(user.xp)
        user.level = new_level
        user.avatar_title = get_title_for_level(new_level)
        return await self._user_repository.update(user)
