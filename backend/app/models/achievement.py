"""Beanie Document models for the Achievement domain."""

from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class Achievement(Document):
    """MongoDB document defining an earnable achievement badge.

    Attributes:
        slug: Unique machine-readable identifier.
        title: Display name shown to the user.
        description: Explanation of how to earn this achievement.
        icon: Emoji or icon identifier for display.
        xp_reward: XP awarded when this achievement is first earned.
        trigger_type: Category of trigger (e.g. "task_count", "streak", "quiz_pass").
        trigger_value: Threshold value for the trigger condition.
    """

    slug: str
    title: str
    description: str = ""
    icon: str = "🏆"
    xp_reward: int = 25
    trigger_type: str
    trigger_value: int = 1

    class Settings:
        name = "achievements"


class UserAchievement(Document):
    """MongoDB document recording an achievement earned by a user.

    Attributes:
        user_id: ID of the user who earned the achievement.
        achievement_id: ID of the Achievement document.
        earned_at: UTC timestamp when the achievement was awarded.
    """

    user_id: str
    achievement_id: str
    earned_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "user_achievements"
