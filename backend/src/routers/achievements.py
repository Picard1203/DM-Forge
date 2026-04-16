"""Achievements router: listing all and user-earned achievements."""

from typing import List

from fastapi import APIRouter, Depends

from src.deps import get_achievement_service, get_current_user
from src.models.user import User
from src.schemas.achievement import AchievementResponse, UserAchievementResponse
from src.services.achievement_service import AchievementService

router = APIRouter(prefix="/api/v1/achievements", tags=["achievements"])


@router.get("", response_model=List[AchievementResponse])
async def list_achievements(
    _current_user: User = Depends(get_current_user),
    achievement_service: AchievementService = Depends(get_achievement_service),
) -> List[AchievementResponse]:
    """Return all achievement definitions.

    Args:
        _current_user (User): Authenticated user (access guard).
        achievement_service (AchievementService): Injected service instance.

    Returns:
        List[AchievementResponse]: List of AchievementResponse objects.
    """
    return await achievement_service.list_all()


@router.get("/mine", response_model=List[UserAchievementResponse])
async def list_my_achievements(
    current_user: User = Depends(get_current_user),
    achievement_service: AchievementService = Depends(get_achievement_service),
) -> List[UserAchievementResponse]:
    """Return achievements earned by the authenticated user.

    Args:
        current_user (User): The authenticated user.
        achievement_service (AchievementService): Injected service instance.

    Returns:
        List[UserAchievementResponse]: Earned achievements with earned_at timestamps.
    """
    return await achievement_service.list_user_achievements(user_id=str(current_user.id))
