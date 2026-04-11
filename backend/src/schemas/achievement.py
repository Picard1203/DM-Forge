"""Pydantic schemas for achievement endpoints."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AchievementResponse(BaseModel):
    """Serialised Achievement definition.

    Attributes:
        id: MongoDB document ID.
        slug: Machine-readable identifier.
        title: Display name.
        description: How to earn this achievement.
        icon: Emoji or icon string.
        xp_reward: XP awarded on first earn.
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
        earned_at: UTC timestamp when the achievement was awarded.
    """

    earned_at: datetime
