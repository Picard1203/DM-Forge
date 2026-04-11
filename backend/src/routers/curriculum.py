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
        _current_user (User): Authenticated user (access guard).
        curriculum_service (CurriculumService): Injected service instance.

    Returns:
        List[ModuleResponse]: Ordered list of ModuleResponse objects.
    """
    modules = await curriculum_service.list_modules()
    responses: List[ModuleResponse] = []
    for module in modules:
        responses.append(
            ModuleResponse(
                id=str(module.id),
                slug=module.slug,
                title=module.title,
                description=module.description,
                order=module.order,
                estimated_minutes=module.estimated_minutes,
                icon=module.icon,
                is_extension=module.is_extension,
            )
        )
    return responses


@router.get("/{module_id}", response_model=ModuleDetailResponse)
async def get_module(
    module_id: str,
    _current_user: User = Depends(get_current_user),
    curriculum_service: CurriculumService = Depends(get_curriculum_service),
) -> ModuleDetailResponse:
    """Return a single module with its ordered task list.

    Args:
        module_id (str): The module's document ID.
        _current_user (User): Authenticated user (access guard).
        curriculum_service (CurriculumService): Injected service instance.

    Returns:
        ModuleDetailResponse: A ModuleDetailResponse with embedded tasks.
    """
    module = await curriculum_service.get_module(module_id)
    tasks = await curriculum_service.get_module_tasks(module_id)
    task_responses: List[TaskResponse] = []
    for task in tasks:
        task_responses.append(
            TaskResponse(
                id=str(task.id),
                module_id=task.module_id,
                slug=task.slug,
                title=task.title,
                task_type=task.task_type,
                content_url=task.content_url,
                description=task.description,
                order=task.order,
                estimated_minutes=task.estimated_minutes,
                xp_reward=task.xp_reward,
                tags=task.tags,
            )
        )
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
        module_id (str): The parent module's document ID.
        _current_user (User): Authenticated user (access guard).
        curriculum_service (CurriculumService): Injected service instance.

    Returns:
        List[TaskResponse]: Ordered list of TaskResponse objects.
    """
    tasks = await curriculum_service.get_module_tasks(module_id)
    responses: List[TaskResponse] = []
    for task in tasks:
        responses.append(
            TaskResponse(
                id=str(task.id),
                module_id=task.module_id,
                slug=task.slug,
                title=task.title,
                task_type=task.task_type,
                content_url=task.content_url,
                description=task.description,
                order=task.order,
                estimated_minutes=task.estimated_minutes,
                xp_reward=task.xp_reward,
                tags=task.tags,
            )
        )
    return responses
