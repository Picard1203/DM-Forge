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
        _user_repository: Injected repository for user data operations.
    """

    def __init__(self, user_repository: AbstractUserRepository) -> None:
        """Initialise the service with a user repository.

        Args:
            user_repository: An AbstractUserRepository implementation.
        """
        self._user_repository = user_repository

    async def register(self, request: RegisterRequest) -> TokenResponse:
        """Register a new user and return a signed JWT.

        Checks for duplicate email and username before creating the account.

        Args:
            request: Validated registration request containing email, username,
                and plain-text password.

        Returns:
            A TokenResponse containing the signed access token.

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
            email: The registered email address.
            password: The plain-text password to verify.

        Returns:
            A TokenResponse containing the signed access token.

        Raises:
            InvalidCredentialsError: If the email is not found or the password
                does not match the stored hash.
        """
        user: Optional[User] = await self._user_repository.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        token = create_access_token(subject=str(user.id))
        return TokenResponse(access_token=token)

    async def get_current_user(self, token: str) -> User:
        """Decode a JWT and return the associated user.

        Args:
            token: A signed JWT access token.

        Returns:
            The User document corresponding to the token's subject claim.

        Raises:
            InvalidCredentialsError: If the token is invalid, expired, or the
                user no longer exists in the database.
        """
        subject: Optional[str] = decode_token(token)
        if subject is None:
            raise InvalidCredentialsError()

        user: Optional[User] = await self._user_repository.get_by_id(subject)
        if user is None:
            raise InvalidCredentialsError()

        return user
