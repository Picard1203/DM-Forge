"""Session service: time-aware session plan builder."""

from typing import List

from src.schemas.session import SessionPlanResponse, SessionRequest, SessionTaskItem
from src.schemas.curriculum import TaskResponse
from src.services.curriculum_service import CurriculumService
from src.services.progress_service import ProgressService


class SessionService:
    """Builds a time-aware session plan from incomplete tasks.

    Attributes:
        _curriculum_service (CurriculumService): Curriculum data service.
        _progress_service (ProgressService): User progress service.
    """

    def __init__(
        self,
        curriculum_service: CurriculumService,
        progress_service: ProgressService,
    ) -> None:
        """Initialise the service with curriculum and progress services.

        Args:
            curriculum_service (CurriculumService): Provides module/task data.
            progress_service (ProgressService): Provides completion state.
        """
        self._curriculum_service = curriculum_service
        self._progress_service = progress_service

    async def build_plan(self, user_id: str, request: SessionRequest) -> SessionPlanResponse:
        """Build a session plan fitting within the requested time budget.

        Args:
            user_id (str): The ID of the user requesting the session.
            request (SessionRequest): Documentation regarding available minutes.

        Returns:
            SessionPlanResponse: Plan with an ordered list of tasks.
        """
        modules = await self._curriculum_service.list_modules()
        budget = request.available_minutes
        remaining = budget
        items: List[SessionTaskItem] = []
        xp_potential = 0
        for module in modules:
            tasks = await self._curriculum_service.get_module_tasks(str(module.id))
            for task in tasks:
                already_done = await self._progress_service.is_task_complete(
                    user_id=user_id, task_id=str(task.id)
                )
                if already_done is False and task.estimated_minutes <= remaining:
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
