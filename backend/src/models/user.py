"""Beanie Document models for the User domain."""

from datetime import UTC, datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, EmailStr, Field


class UserSettings(BaseModel):
    """Embedded document storing per-user application preferences.

    Attributes:
        rotation_interval_minutes (int): Minutes between content rotation prompts.
    """

    rotation_interval_minutes: int = 20


class User(Document):
    """MongoDB document representing a registered user.

    Attributes:
        email (EmailStr): Unique email address used for authentication.
        username (str): Unique display name chosen at registration.
        hashed_password (str): bcrypt hash of the user's password.
        avatar_title (str): Gamification title shown on the user's profile.
        xp (int): Total experience points accumulated.
        level (int): Current level derived from XP.
        current_streak (int): Consecutive days of activity.
        longest_streak (int): Historical maximum streak.
        last_activity_date (Optional[datetime]): UTC timestamp of last activity.
        settings (UserSettings): Embedded user preference document.
        created_at (datetime): UTC timestamp of document creation.
        updated_at (datetime): UTC timestamp of last modification.
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
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "users"
