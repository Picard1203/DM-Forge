"""Curriculum router: module and task listing endpoints."""

from typing import List

from fastapi import APIRouter, Depends

from src.deps import get_curriculum_service, get_current_user
from src.models.user import User
from src.schemas.curriculum import ModuleDetailResponse, ModuleResponse, TaskResponse
from src.services.curriculum_service import CurriculumService

router = APIRouter(prefix="/api/v1/modules", tags=["curriculum"])


@router.get("", response_model=List[ModuleResponse])
async def list_modules(
    _current_user: User = Depends(get_current_user),
    curriculum_service: CurriculumService = Depends(get_curriculum_service),
) -> List[ModuleResponse]:
    """Return all modules ordered by their position in the curriculum.

    Args:
        _current_user: Authenticated user (access guard).
        curriculum_service: Injected CurriculumService instance.

    Returns:
        Ordered list of ModuleResponse objects.
    """
    modules = await curriculum_service.list_modules()
    return [
        ModuleResponse(
            id=str(m.id),
            slug=m.slug,
            title=m.title,
            description=m.description,
            order=m.order,
            estimated_minutes=m.estimated_minutes,
            icon=m.icon,
            is_extension=m.is_extension,
        )
        for m in modules
    ]


@router.get("/{module_id}", response_model=ModuleDetailResponse)
async def get_module(
    module_id: str,
    _current_user: User = Depends(get_current_user),
    curriculum_service: CurriculumService = Depends(get_curriculum_service),
) -> ModuleDetailResponse:
    """Return a single module with its ordered task list.

    Args:
        module_id: The module's document ID.
        _current_user: Authenticated user (access guard).
        curriculum_service: Injected CurriculumService instance.

    Returns:
        A ModuleDetailResponse with embedded tasks.
    """
    module = await curriculum_service.get_module(module_id)
    tasks = await curriculum_service.get_module_tasks(module_id)
    task_responses = [
        TaskResponse(
            id=str(t.id),
            module_id=t.module_id,
            slug=t.slug,
            title=t.title,
            task_type=t.task_type,
            content_url=t.content_url,
            description=t.description,
            order=t.order,
            estimated_minutes=t.estimated_minutes,
            xp_reward=t.xp_reward,
            tags=t.tags,
        )
        for t in tasks
    ]
    return ModuleDetailResponse(
        id=str(module.id),
        slug=module.slug,
        title=module.title,
        description=module.description,
        order=module.order,
        estimated_minutes=module.estimated_minutes,
        icon=module.icon,
        is_extension=module.is_extension,
        tasks=task_responses,
    )


@router.get("/{module_id}/tasks", response_model=List[TaskResponse])
async def list_module_tasks(
    module_id: str,
    _current_user: User = Depends(get_current_user),
    curriculum_service: CurriculumService = Depends(get_curriculum_service),
) -> List[TaskResponse]:
    """Return all tasks for a module ordered by position.

    Args:
        module_id: The parent module's document ID.
        _current_user: Authenticated user (access guard).
        curriculum_service: Injected CurriculumService instance.

    Returns:
        Ordered list of TaskResponse objects.
    """
    tasks = await curriculum_service.get_module_tasks(module_id)
    return [
        TaskResponse(
            id=str(t.id),
            module_id=t.module_id,
            slug=t.slug,
            title=t.title,
            task_type=t.task_type,
            content_url=t.content_url,
            description=t.description,
            order=t.order,
            estimated_minutes=t.estimated_minutes,
            xp_reward=t.xp_reward,
            tags=t.tags,
        )
        for t in tasks
    ]
