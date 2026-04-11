"""Tests for XP calculation, levelling, and streak logic.

Stubs — full implementation pending user fixture extensions.
"""

import pytest


@pytest.mark.asyncio
async def test_xp_award_increases_user_xp() -> None:
    """Awarding XP increases the user's total xp field. (stub)"""
    pass


@pytest.mark.asyncio
async def test_level_up_changes_title() -> None:
    """Reaching a level threshold updates avatar_title. (stub)"""
    pass


@pytest.mark.asyncio
async def test_streak_increments_on_consecutive_day() -> None:
    """Activity on consecutive days increments current_streak. (stub)"""
    pass


@pytest.mark.asyncio
async def test_streak_resets_after_missed_day() -> None:
    """Missing a day resets current_streak to 1. (stub)"""
    pass
