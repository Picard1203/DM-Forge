"""Beanie Document models for the User domain."""

from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, EmailStr, Field


class UserSettings(BaseModel):
    """Embedded document storing per-user application preferences.

    Attributes:
        rotation_interval_minutes: Minutes between content rotation prompts.
    """

    rotation_interval_minutes: int = 20


class User(Document):
    """MongoDB document representing a registered user.

    Attributes:
        email: Unique email address used for authentication.
        username: Unique display name chosen at registration.
        hashed_password: bcrypt hash of the user's password.
        avatar_title: Gamification title shown on the user's profile.
        xp: Total experience points accumulated.
        level: Current level derived from XP.
        current_streak: Consecutive days of activity.
        longest_streak: Historical maximum streak.
        last_activity_date: UTC timestamp of last recorded activity.
        settings: Embedded user preference document.
        created_at: UTC timestamp of document creation.
        updated_at: UTC timestamp of last modification.
    """

    email: EmailStr
    username: str
    hashed_password: str
    avatar_title: str = "Apprentice"
    xp: int = 0
    level: int = 1
    current_streak: int = 0
    longest_streak: int = 0
    last_activity_date: Optional[datetime] = None
    settings: UserSettings = Field(default_factory=UserSettings)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
