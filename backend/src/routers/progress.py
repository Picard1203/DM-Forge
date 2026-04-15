"""Progress router: task completion and overview endpoints."""

from fastapi import APIRouter, Depends, status
from typing import List

from src.deps import get_current_user, get_curriculum_service, get_progress_service
from src.models.curriculum import Module
from src.models.user import User
from src.schemas.progress import CompleteTaskRequest, CompleteTaskResponse, ProgressOverviewResponse
from src.services.curriculum_service import CurriculumService
from src.services.progress_service import ProgressService

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])


@router.post(
    "/complete",
    status_code=status.HTTP_200_OK,
    response_model=CompleteTaskResponse,
)
async def complete_task(
    request: CompleteTaskRequest,
    current_user: User = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service),
) -> CompleteTaskResponse:
    """Mark a task as complete and award XP to the user.

    Args:
        request (CompleteTaskRequest): Task ID to mark complete.
        current_user (User): The authenticated user.
        progress_service (ProgressService): Injected ProgressService instance.

    Returns:
        CompleteTaskResponse: XP earned and updated user stats.
    """
    return await progress_service.complete_task(
        user=current_user, task_id=request.task_id
    )


@router.get("/overview", response_model=ProgressOverviewResponse)
async def get_overview(
    current_user: User = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service),
    curriculum_service: CurriculumService = Depends(get_curriculum_service),
) -> ProgressOverviewResponse:
    """Return a full progress overview for the authenticated user.

    Args:
        current_user (User): The authenticated user.
        progress_service (ProgressService): Injected ProgressService instance.
        curriculum_service (CurriculumService): Injected CurriculumService instance.

    Returns:
        ProgressOverviewResponse: Overview with per-module and aggregate data.
    """
    all_modules: List[Module] = await curriculum_service.get_all_modules()
    return await progress_service.get_overview(
        user_id=str(current_user.id), all_modules=all_modules
    )
