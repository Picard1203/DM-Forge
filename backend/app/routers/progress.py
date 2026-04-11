"""Progress router: task completion and overview endpoints."""

from fastapi import APIRouter, Depends, status

from app.deps import get_current_user, get_gamification_service, get_progress_service
from app.models.user import User
from app.schemas.progress import CompleteTaskRequest, ProgressOverviewResponse
from app.services.gamification_service import GamificationService
from app.services.progress_service import ProgressService

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])


@router.post("/complete", status_code=status.HTTP_200_OK)
async def complete_task(
    request: CompleteTaskRequest,
    current_user: User = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service),
    gamification_service: GamificationService = Depends(get_gamification_service),
) -> dict:
    """Mark a task as complete and award XP to the user.

    Args:
        request: Task and module IDs to mark complete.
        current_user: The authenticated user.
        progress_service: Injected ProgressService instance.
        gamification_service: Injected GamificationService instance.

    Returns:
        A dict with xp_awarded and a confirmation message.
    """
    xp_awarded = await progress_service.complete_task(
        user_id=str(current_user.id), request=request
    )
    if xp_awarded > 0:
        await gamification_service.award_xp_and_check(
            user=current_user, xp_amount=xp_awarded
        )
    return {"xp_awarded": xp_awarded, "message": "Task recorded."}


@router.get("/overview", response_model=ProgressOverviewResponse)
async def get_overview(
    current_user: User = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service),
) -> ProgressOverviewResponse:
    """Return a full progress overview for the authenticated user.

    Args:
        current_user: The authenticated user.
        progress_service: Injected ProgressService instance.

    Returns:
        A ProgressOverviewResponse with per-module and aggregate data.
    """
    return await progress_service.get_overview(user_id=str(current_user.id))
