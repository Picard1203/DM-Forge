"""Authentication router: register and login endpoints."""

from fastapi import APIRouter, Depends, status

from src.deps import get_auth_service, get_current_user
from src.models.user import User
from src.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from src.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Register a new user account and return an access token.

    Args:
        request (RegisterRequest): Validated registration payload.
        auth_service (AuthService): Injected AuthService instance.

    Returns:
        TokenResponse: A TokenResponse containing the signed JWT.
    """
    return await auth_service.register(request)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Authenticate with email and password and return an access token.

    Args:
        request (LoginRequest): Validated login payload.
        auth_service (AuthService): Injected AuthService instance.

    Returns:
        TokenResponse: A TokenResponse containing the signed JWT.
    """
    return await auth_service.login(email=request.email, password=request.password)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return the profile of the currently authenticated user.

    Args:
        current_user (User): The user resolved from the Bearer token.

    Returns:
        UserResponse: A UserResponse with the user's public profile fields.
    """
    return UserResponse(
        id=str(current_user.id),
        email=str(current_user.email),
        username=current_user.username,
        avatar_title=current_user.avatar_title,
        xp=current_user.xp,
        level=current_user.level,
        current_streak=current_user.current_streak,
        longest_streak=current_user.longest_streak,
    )
