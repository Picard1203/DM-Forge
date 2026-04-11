"""Pydantic request/response schemas for authentication endpoints."""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Request body for the registration endpoint.

    Attributes:
        email: The user's email address.
        username: Chosen display name (3–30 characters).
        password: Plain-text password (min 8 characters).
    """

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    """Request body for the login endpoint.

    Attributes:
        email: The registered email address.
        password: The plain-text password.
    """

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response body returned after successful authentication.

    Attributes:
        access_token: Signed JWT access token.
        token_type: Always ``"bearer"``.
    """

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Serialised user returned from the /me endpoint.

    Attributes:
        id: MongoDB document ID as a string.
        email: The user's email address.
        username: The user's display name.
        avatar_title: Current gamification title.
        xp: Total experience points.
        level: Current level.
        current_streak: Consecutive active days.
        longest_streak: Historical maximum streak.
    """

    id: str
    email: str
    username: str
    avatar_title: str
    xp: int
    level: int
    current_streak: int
    longest_streak: int
