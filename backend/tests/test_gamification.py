"""Tests for GamificationService: XP award, level-up, and streak logic."""

from datetime import UTC, datetime, timedelta

import pytest

from src.models.user import User
from src.repositories.mongodb.user_repository import MongoUserRepository
from src.services.gamification_service import GamificationService, XP_THRESHOLDS
from src.utils.security import get_password_hash


async def _make_user(suffix: str = "") -> User:
    """Insert and return a fresh test user.

    Args:
        suffix (str): Optional suffix to make email/username unique.

    Returns:
        User: The inserted User document.
    """
    user = User(
        email=f"gami{suffix}@test.com",
        username=f"GamiUser{suffix}",
        hashed_password=get_password_hash("TestPass1!"),
    )
    await user.insert()
    return user


@pytest.mark.asyncio
async def test_xp_award_increases_user_xp() -> None:
    """award_xp adds the given amount to user.xp and persists it."""
    user = await _make_user("xp")
    service = GamificationService(user_repository=MongoUserRepository())
    updated = await service.award_xp(user, 100)
    assert updated.xp == 100
    refreshed = await User.get(updated.id)
    assert refreshed.xp == 100


@pytest.mark.asyncio
async def test_level_up_changes_title() -> None:
    """award_xp reaching level-5 threshold sets title to Journeyman."""
    user = await _make_user("lvl")
    service = GamificationService(user_repository=MongoUserRepository())
    xp_for_level_5 = XP_THRESHOLDS[4]
    updated = await service.award_xp(user, xp_for_level_5)
    assert updated.level == 5
    assert updated.avatar_title == "Journeyman"


@pytest.mark.asyncio
async def test_streak_increments_on_consecutive_day() -> None:
    """update_streak increments current_streak when last activity was yesterday."""
    user = await _make_user("streak_inc")
    user.current_streak = 3
    user.longest_streak = 3
    user.last_activity_date = datetime.now(UTC) - timedelta(days=1)
    await user.save()
    service = GamificationService(user_repository=MongoUserRepository())
    updated = await service.update_streak(user)
    assert updated.current_streak == 4
    assert updated.longest_streak == 4


@pytest.mark.asyncio
async def test_streak_resets_after_missed_day() -> None:
    """update_streak resets current_streak to 1 when more than one day has passed."""
    user = await _make_user("streak_reset")
    user.current_streak = 5
    user.longest_streak = 5
    user.last_activity_date = datetime.now(UTC) - timedelta(days=3)
    await user.save()
    service = GamificationService(user_repository=MongoUserRepository())
    updated = await service.update_streak(user)
    assert updated.current_streak == 1
    assert updated.longest_streak == 5
