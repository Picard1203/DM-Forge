"""Achievements router: listing all and user-earned achievements."""

from typing import List

from fastapi import APIRouter, Depends

from src.deps import get_achievement_service, get_current_user
from src.models.user import User
from src.schemas.achievement import AchievementResponse
from src.services.achievement_service import AchievementService

router = APIRouter(prefix="/api/v1/achievements", tags=["achievements"])


@router.get("", response_model=List[AchievementResponse])
async def list_achievements(
    _current_user: User = Depends(get_current_user),
    achievement_service: AchievementService = Depends(get_achievement_service),
) -> List[AchievementResponse]:
    """Return all achievement definitions.

    Args:
        _current_user: Authenticated user (access guard).
        achievement_service: Injected AchievementService instance.

    Returns:
        List of AchievementResponse objects.
    """
    return await achievement_service.list_all()


@router.get("/mine", response_model=List[AchievementResponse])
async def list_my_achievements(
    current_user: User = Depends(get_current_user),
    achievement_service: AchievementService = Depends(get_achievement_service),
) -> List[AchievementResponse]:
    """Return achievements earned by the authenticated user.

    Args:
        current_user: The authenticated user.
        achievement_service: Injected AchievementService instance.

    Returns:
        List of AchievementResponse objects for earned achievements.

    Note:
        Full implementation pending join logic in AchievementService.
    """
    # TODO: return full UserAchievementResponse once join is implemented
    return []
