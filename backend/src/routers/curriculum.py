"""Curriculum router: module and task listing endpoints."""

from typing import List

from fastapi import APIRouter, Depends

from src.deps import get_curriculum_service, get_current_user
from src.models.curriculum import Module, Task
from src.models.user import User
from src.schemas.curriculum import ModuleResponse, TaskResponse
from src.services.curriculum_service import CurriculumService

router = APIRouter(prefix="/api/v1/modules", tags=["curriculum"])


def _module_to_response(module: Module) -> ModuleResponse:
    """Convert a Module document to its API response shape.

    Args:
        module (Module): The Module document to serialise.

    Returns:
        (ModuleResponse): A ModuleResponse populated from the document fields.
    """
    return ModuleResponse(
        id=str(module.id),
        slug=module.slug,
        title=module.title,
        description=module.description,
        order=module.order,
        icon=module.icon,
        is_extension=module.is_extension,
        estimated_hours=module.estimated_hours,
        xp_reward=module.xp_reward,
    )


def _task_to_response(task: Task) -> TaskResponse:
    """Convert a Task document to its API response shape.

    Args:
        task (Task): The Task document to serialise.

    Returns:
        (TaskResponse): A TaskResponse populated from the document fields.
    """
    return TaskResponse(
        id=str(task.id),
        slug=task.slug,
        title=task.title,
        description=task.description,
        order=task.order,
        task_type=task.task_type,
        estimated_minutes=task.estimated_minutes,
        xp_reward=task.xp_reward,
        content=task.content,
    )


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
        (List[ModuleResponse]): Ordered list of ModuleResponse objects.
    """
    modules = await curriculum_service.get_all_modules()
    responses: List[ModuleResponse] = []
    for module in modules:
        responses.append(_module_to_response(module))
    return responses


@router.get("/{slug}", response_model=ModuleResponse)
async def get_module(
    slug: str,
    _current_user: User = Depends(get_current_user),
    curriculum_service: CurriculumService = Depends(get_curriculum_service),
) -> ModuleResponse:
    """Return a single module by its URL slug.

    Args:
        slug (str): The module's URL-safe slug.
        _current_user (User): Authenticated user (access guard).
        curriculum_service (CurriculumService): Injected service instance.

    Returns:
        (ModuleResponse): The matching module serialised as a ModuleResponse.
    """
    module = await curriculum_service.get_module_by_slug(slug)
    return _module_to_response(module)


@router.get("/{slug}/tasks", response_model=List[TaskResponse])
async def list_module_tasks(
    slug: str,
    _current_user: User = Depends(get_current_user),
    curriculum_service: CurriculumService = Depends(get_curriculum_service),
) -> List[TaskResponse]:
    """Return all tasks for a module identified by slug, ordered by position.

    Args:
        slug (str): The parent module's URL-safe slug.
        _current_user (User): Authenticated user (access guard).
        curriculum_service (CurriculumService): Injected service instance.

    Returns:
        (List[TaskResponse]): Ordered list of TaskResponse objects.
    """
    tasks = await curriculum_service.get_tasks_for_module(slug)
    responses: List[TaskResponse] = []
    for task in tasks:
        responses.append(_task_to_response(task))
    return responses
