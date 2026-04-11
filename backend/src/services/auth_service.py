"""Authentication service: registration, login, and token verification."""

from typing import Optional

from src.models.user import User
from src.repositories.abstract.user_repository import AbstractUserRepository
from src.schemas.auth import RegisterRequest, TokenResponse
from src.utils.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
)
from src.utils.security import create_access_token, decode_token, get_password_hash, verify_password


class AuthService:
    """Handles all authentication-related business logic.

    Attributes:
        _user_repository (AbstractUserRepository): Injected repository for user data.
    """

    def __init__(self, user_repository: AbstractUserRepository) -> None:
        """Initialise the service with a user repository.

        Args:
            user_repository (AbstractUserRepository): An AbstractUserRepository implementation.
        """
        self._user_repository = user_repository

    async def register(self, request: RegisterRequest) -> TokenResponse:
        """Register a new user and return a signed JWT.

        Args:
            request (RegisterRequest): Validated registration payload.

        Returns:
            TokenResponse: A TokenResponse containing the signed access token.

        Raises:
            EmailAlreadyExistsError: If the email is already registered.
            UsernameAlreadyExistsError: If the username is already taken.
        """
        existing_email: Optional[User] = await self._user_repository.get_by_email(request.email)
        if existing_email is not None:
            raise EmailAlreadyExistsError()
        existing_username: Optional[User] = await self._user_repository.get_by_username(
            request.username
        )
        if existing_username is not None:
            raise UsernameAlreadyExistsError()
        user = User(
            email=request.email,
            username=request.username,
            hashed_password=get_password_hash(request.password),
        )
        created_user = await self._user_repository.create(user)
        token = create_access_token(subject=str(created_user.id))
        return TokenResponse(access_token=token)

    async def login(self, email: str, password: str) -> TokenResponse:
        """Authenticate a user and return a signed JWT.

        Args:
            email (str): The registered email address.
            password (str): The plain-text password to verify.

        Returns:
            TokenResponse: A TokenResponse containing the signed access token.

        Raises:
            InvalidCredentialsError: If the email is not found or password mismatch.
        """
        user: Optional[User] = await self._user_repository.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError()
        if verify_password(password, user.hashed_password) is False:
            raise InvalidCredentialsError()
        token = create_access_token(subject=str(user.id))
        return TokenResponse(access_token=token)

    async def get_current_user(self, token: str) -> User:
        """Decode a JWT and return the associated user.

        Args:
            token (str): A signed JWT access token.

        Returns:
            User: The User document corresponding to the token subject.

        Raises:
            InvalidCredentialsError: If the token is invalid or user missing.
        """
        subject: Optional[str] = decode_token(token)
        if subject is None:
            raise InvalidCredentialsError()
        user: Optional[User] = await self._user_repository.get_by_id(subject)
        if user is None:
            raise InvalidCredentialsError()
        return user
