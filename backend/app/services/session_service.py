"""Session service: time-aware session plan builder."""

from typing import List

from app.schemas.session import SessionPlanResponse, SessionRequest, SessionTaskItem
from app.schemas.curriculum import TaskResponse
from app.services.curriculum_service import CurriculumService
from app.services.progress_service import ProgressService


class SessionService:
    """Builds a time-aware session plan from incomplete tasks.

    Attributes:
        _curriculum_service: Injected curriculum service.
        _progress_service: Injected progress service.
    """

    def __init__(
        self,
        curriculum_service: CurriculumService,
        progress_service: ProgressService,
    ) -> None:
        """Initialise the service with curriculum and progress services.

        Args:
            curriculum_service: Provides module and task data.
            progress_service: Provides completion state per user.
        """
        self._curriculum_service = curriculum_service
        self._progress_service = progress_service

    async def build_plan(self, user_id: str, request: SessionRequest) -> SessionPlanResponse:
        """Build a session plan fitting within the requested time budget.

        Selects incomplete tasks in module order, adding them until the time
        budget would be exceeded.

        Args:
            user_id: The ID of the user requesting the session.
            request: Contains the number of available minutes.

        Returns:
            A SessionPlanResponse with an ordered list of tasks and totals.
        """
        modules = await self._curriculum_service.list_modules()
        budget = request.available_minutes
        remaining = budget
        items: List[SessionTaskItem] = []
        xp_potential = 0

        for module in modules:
            tasks = await self._curriculum_service.get_module_tasks(str(module.id))
            for task in tasks:
                already_done = await self._progress_service._progress_repository.is_task_complete(
                    user_id=user_id, task_id=str(task.id)
                )
                if already_done is True:
                    continue
                if task.estimated_minutes > remaining:
                    continue
                task_response = TaskResponse(
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
                items.append(
                    SessionTaskItem(
                        task=task_response,
                        estimated_minutes=task.estimated_minutes,
                    )
                )
                remaining -= task.estimated_minutes
                xp_potential += task.xp_reward

        return SessionPlanResponse(
            items=items,
            total_minutes=budget - remaining,
            xp_potential=xp_potential,
        )
