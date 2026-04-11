"""Pydantic request/response schemas for authentication endpoints."""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Request body for the registration endpoint.

    Attributes:
        email (EmailStr): The user's email address.
        username (str): Chosen display name (3–30 characters).
        password (str): Plain-text password (min 8 characters).
    """

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    """Request body for the login endpoint.

    Attributes:
        email (EmailStr): The registered email address.
        password (str): The plain-text password.
    """

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response body returned after successful authentication.

    Attributes:
        access_token (str): Signed JWT access token.
        token_type (str): Always bearer.
    """

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Serialised user returned from the authenticated profile endpoint.

    Attributes:
        id (str): MongoDB document ID as a string.
        email (str): The user's email address.
        username (str): The user's display name.
        avatar_title (str): Current gamification title.
        xp (int): Total experience points.
        level (int): Current level.
        current_streak (int): Consecutive active days.
        longest_streak (int): Historical maximum streak.
    """

    id: str
    email: str
    username: str
    avatar_title: str
    xp: int
    level: int
    current_streak: int
    longest_streak: int
