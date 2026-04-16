"""Tests for achievement trigger checking and awarding."""

import pytest
from httpx import AsyncClient

from src.models.achievement import Achievement, UserAchievement
from src.repositories.mongodb.achievement_repository import MongoAchievementRepository
from src.services.achievement_service import AchievementService


async def _seed_achievement(
    slug: str,
    trigger_type: str,
    trigger_value: str,
    xp_reward: int = 50,
) -> Achievement:
    """Insert and return a single Achievement document.

    Args:
        slug (str): Unique achievement slug.
        trigger_type (str): Trigger category.
        trigger_value (str): Threshold or value required to earn.
        xp_reward (int): XP awarded on earning.

    Returns:
        Achievement: The inserted Achievement document.
    """
    achievement = Achievement(
        slug=slug,
        title=slug.replace("-", " ").title(),
        description="Test achievement",
        icon="award",
        trigger_type=trigger_type,
        trigger_value=trigger_value,
        xp_reward=xp_reward,
    )
    await achievement.insert()
    return achievement


@pytest.mark.asyncio
async def test_achievement_awarded_on_trigger_threshold(
    mock_user,
) -> None:
    """Achievement is awarded when event_value meets the numeric trigger_value."""
    await _seed_achievement(
        slug="first-blood",
        trigger_type="tasks_completed",
        trigger_value="10",
        xp_reward=50,
    )
    service = AchievementService(achievement_repository=MongoAchievementRepository())
    earned = await service.check_and_award(
        user_id=str(mock_user.id),
        event_type="tasks_completed",
        event_value="10",
    )
    assert len(earned) == 1
    assert earned[0].slug == "first-blood"
    user_achievements = await UserAchievement.find(
        UserAchievement.user_id == str(mock_user.id)
    ).to_list()
    assert len(user_achievements) == 1


@pytest.mark.asyncio
async def test_achievement_not_awarded_twice(
    mock_user,
) -> None:
    """Achievement is not awarded a second time if already earned."""
    achievement = await _seed_achievement(
        slug="first-blood",
        trigger_type="tasks_completed",
        trigger_value="10",
    )
    existing = UserAchievement(
        user_id=str(mock_user.id),
        achievement_id=str(achievement.id),
    )
    await existing.insert()
    service = AchievementService(achievement_repository=MongoAchievementRepository())
    earned = await service.check_and_award(
        user_id=str(mock_user.id),
        event_type="tasks_completed",
        event_value="15",
    )
    assert len(earned) == 0
    user_achievements = await UserAchievement.find(
        UserAchievement.user_id == str(mock_user.id)
    ).to_list()
    assert len(user_achievements) == 1


@pytest.mark.asyncio
async def test_list_achievements_returns_all(
    client: AsyncClient,
    auth_token: str,
) -> None:
    """GET /achievements returns all seeded achievement definitions."""
    await _seed_achievement("ach-one", "tasks_completed", "10")
    await _seed_achievement("ach-two", "streak", "7")
    await _seed_achievement("ach-three", "module_complete", "rules-fundamentals")
    response = await client.get(
        "/api/v1/achievements",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    slugs = [item["slug"] for item in data]
    assert "ach-one" in slugs
    assert "ach-two" in slugs
    assert "ach-three" in slugs
    for item in data:
        assert "id" in item
        assert "icon" in item
        assert "xp_reward" in item
