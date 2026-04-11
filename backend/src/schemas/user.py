"""Pydantic schemas for user profile endpoints."""

from typing import Optional

from pydantic import BaseModel, Field


class UserSettingsUpdate(BaseModel):
    """Partial update for embedded user settings.

    Attributes:
        rotation_interval_minutes: Minutes between content rotation prompts.
    """

    rotation_interval_minutes: Optional[int] = Field(None, ge=5, le=120)


class UserUpdate(BaseModel):
    """Request body for updating a user's profile.

    Attributes:
        username: New display name.
        settings: Partial settings update.
    """

    username: Optional[str] = Field(None, min_length=3, max_length=30)
    settings: Optional[UserSettingsUpdate] = None


class UserStatsResponse(BaseModel):
    """Response body for the user stats endpoint.

    Attributes:
        xp: Total experience points.
        level: Current level.
        current_streak: Consecutive active days.
        longest_streak: Historical maximum streak.
        avatar_title: Current gamification title.
        tasks_completed_total: Total tasks completed across all modules.
    """

    xp: int
    level: int
    current_streak: int
    longest_streak: int
    avatar_title: str
    tasks_completed_total: int
