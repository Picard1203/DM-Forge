"""Security utilities: JWT creation/decoding and password hashing."""

from datetime import UTC, datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from src.config import settings


def get_password_hash(plain_password: str) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        plain_password (str): The raw password string.

    Returns:
        str: A bcrypt hash string.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored bcrypt hash.

    Args:
        plain_password (str): The raw password to verify.
        hashed_password (str): The stored bcrypt hash.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token.

    Args:
        subject (str): Value for the token sub claim.
        expires_delta (Optional[timedelta]): Custom expiry duration.

    Returns:
        str: A signed JWT string.
    """
    if expires_delta is not None:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> Optional[str]:
    """Decode a JWT and return the subject claim.

    Args:
        token (str): The JWT string to decode.

    Returns:
        Optional[str]: The sub claim value, or None if invalid.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        subject: Optional[str] = payload.get("sub")
        return subject
    except JWTError:
        return None
