"""Beanie Document models for the Achievement domain."""

from datetime import UTC, datetime

from beanie import Document
from pydantic import Field


class Achievement(Document):
    """MongoDB document defining an achievement and its award criteria.

    Attributes:
        slug (str): Unique URL-friendly identifier.
        title (str): Human-readable achievement name.
        description (str): Detailed text explaining how to earn it.
        icon (str): Icon identifier string for the frontend.
        trigger_type (str): Event category (module_complete, quiz_perfect, streak,
            xp_threshold, tasks_completed).
        trigger_value (str): The value required to unlock the achievement.
        xp_reward (int): XP awarded when the achievement is first earned.
    """

    slug: str
    title: str
    description: str = ""
    icon: str = "award"
    trigger_type: str
    trigger_value: str
    xp_reward: int = 0

    class Settings:
        name = "achievements"


class UserAchievement(Document):
    """MongoDB record of an achievement earned by a specific user.

    Attributes:
        user_id (str): ID of the user.
        achievement_id (str): ID of the Achievement.
        earned_at (datetime): UTC timestamp when awarded.
    """

    user_id: str
    achievement_id: str
    earned_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "user_achievements"
