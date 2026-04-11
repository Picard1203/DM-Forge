"""Pydantic schemas for achievement endpoints."""

from datetime import datetime

from pydantic import BaseModel


class AchievementResponse(BaseModel):
    """Serialised Achievement definition.

    Attributes:
        id (str): MongoDB document ID.
        slug (str): Machine-readable identifier.
        title (str): Display name.
        description (str): How to earn this achievement.
        icon (str): Emoji or icon string.
        xp_reward (int): XP awarded on first earn.

    """

    id: str
    slug: str
    title: str
    description: str
    icon: str
    xp_reward: int


class UserAchievementResponse(AchievementResponse):
    """Achievement with the date it was earned by the current user.

    Attributes:
        earned_at (datetime): UTC timestamp when the achievement was awarded.

    """

    earned_at: datetime
