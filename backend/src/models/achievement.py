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
        trigger_type (str): Category of trigger (e.g. xp_total, level, streak).
        trigger_threshold (int): The value required to unlock the achievement.
        icon_slug (str): Identifier for the frontend icon asset.
    """

    slug: str
    title: str
    description: str = ""
    trigger_type: str
    trigger_threshold: int
    icon_slug: str = "default_medal"

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
