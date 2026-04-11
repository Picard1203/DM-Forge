"""Users router: profile and stats endpoints."""

from fastapi import APIRouter, Depends

from app.deps import get_current_user, get_user_service
from app.models.user import User
from app.schemas.auth import UserResponse
from app.schemas.user import UserStatsResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return the authenticated user's profile.

    Args:
        current_user: The user resolved from the Bearer token.

    Returns:
        A UserResponse with the user's public profile fields.
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


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    update: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Update the authenticated user's profile.

    Args:
        update: Partial update payload.
        current_user: The user resolved from the Bearer token.
        user_service: Injected UserService instance.

    Returns:
        The updated UserResponse.
    """
    updated = await user_service.update_profile(user=current_user, update=update)
    return UserResponse(
        id=str(updated.id),
        email=str(updated.email),
        username=updated.username,
        avatar_title=updated.avatar_title,
        xp=updated.xp,
        level=updated.level,
        current_streak=updated.current_streak,
        longest_streak=updated.longest_streak,
    )


@router.get("/me/stats", response_model=UserStatsResponse)
async def get_my_stats(current_user: User = Depends(get_current_user)) -> UserStatsResponse:
    """Return gamification stats for the authenticated user.

    Args:
        current_user: The user resolved from the Bearer token.

    Returns:
        A UserStatsResponse with XP, level, streak, and title data.
    """
    # tasks_completed_total will be wired up via ProgressService in a future step
    return UserStatsResponse(
        xp=current_user.xp,
        level=current_user.level,
        current_streak=current_user.current_streak,
        longest_streak=current_user.longest_streak,
        avatar_title=current_user.avatar_title,
        tasks_completed_total=0,
    )
