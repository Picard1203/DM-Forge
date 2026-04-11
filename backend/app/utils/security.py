"""Security utilities: JWT creation/decoding and password hashing."""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(plain_password: str) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        plain_password: The raw password string provided by the user.

    Returns:
        A bcrypt hash string suitable for storage.
    """
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored bcrypt hash.

    Args:
        plain_password: The raw password to verify.
        hashed_password: The stored bcrypt hash to compare against.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    return _pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token.

    Args:
        subject: The value to embed in the token's ``sub`` claim (typically a
            user ID or email).
        expires_delta: Optional custom expiry duration. Defaults to the value
            configured in settings.

    Returns:
        A signed JWT string.
    """
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> Optional[str]:
    """Decode a JWT and return the subject claim.

    Args:
        token: The JWT string to decode.

    Returns:
        The ``sub`` claim value if the token is valid, or None if decoding fails.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        subject: Optional[str] = payload.get("sub")
        return subject
    except JWTError:
        return None
