"""Session service: time-aware session plan builder."""

from typing import List

from src.models.curriculum import Task
from src.models.progress import UserProgress
from src.repositories.abstract.module_repository import AbstractModuleRepository
from src.repositories.abstract.progress_repository import AbstractProgressRepository
from src.repositories.abstract.task_repository import AbstractTaskRepository
from src.schemas.session import SessionPlanResponse, SessionTaskItem

_REVIEW_SLOT_MINUTES: int = 5
_MIN_REMAINING_MINUTES: int = 5


class SessionService:
    """Builds a time-aware session plan from the user's incomplete tasks.

    Attributes:
        _module_repository (AbstractModuleRepository): Repository for modules.
        _task_repository (AbstractTaskRepository): Repository for tasks.
        _progress_repository (AbstractProgressRepository): Repository for progress.
    """

    def __init__(
        self,
        module_repository: AbstractModuleRepository,
        task_repository: AbstractTaskRepository,
        progress_repository: AbstractProgressRepository,
    ) -> None:
        """Initialise the service with required repositories.

        Args:
            module_repository (AbstractModuleRepository): Module repository.
            task_repository (AbstractTaskRepository): Task repository.
            progress_repository (AbstractProgressRepository): Progress repository.
        """
        self._module_repository = module_repository
        self._task_repository = task_repository
        self._progress_repository = progress_repository

    async def build_plan(
        self, user_id: str, available_minutes: int
    ) -> SessionPlanResponse:
        """Build a session plan fitting within the requested time budget.

        Args:
            user_id (str): The ID of the user requesting the session.
            available_minutes (int): Total minutes the user has available.

        Returns:
            SessionPlanResponse: Plan with an ordered task list and metadata.
        """
        has_review_slot = available_minutes >= 15
        budget = available_minutes - _REVIEW_SLOT_MINUTES if has_review_slot else available_minutes
        all_tasks = await self._get_all_tasks_ordered()
        incomplete_tasks = await self._get_incomplete_tasks(
            user_id=user_id, all_tasks=all_tasks
        )
        selected_tasks = self._fill_time_budget(
            tasks=incomplete_tasks, budget_minutes=budget
        )
        total_minutes = 0
        for task in selected_tasks:
            total_minutes += task.estimated_minutes
        task_items = self._to_task_items(selected_tasks)
        return SessionPlanResponse(
            tasks=task_items,
            total_minutes=total_minutes,
            has_review_slot=has_review_slot,
        )

    async def _get_all_tasks_ordered(self) -> List[Task]:
        """Fetch all tasks across all modules, ordered by module then task order.

        Returns:
            List[Task]: All tasks in curriculum order.
        """
        modules = await self._module_repository.get_all()
        all_tasks: List[Task] = []
        for module in modules:
            tasks = await self._task_repository.get_by_module_id(
                module_id=str(module.id)
            )
            for task in tasks:
                all_tasks.append(task)
        return all_tasks

    async def _get_incomplete_tasks(
        self, user_id: str, all_tasks: List[Task]
    ) -> List[Task]:
        """Filter out tasks the user has already completed.

        Args:
            user_id (str): The user's document ID.
            all_tasks (List[Task]): All tasks in curriculum order.

        Returns:
            List[Task]: Tasks that have not yet been completed by the user.
        """
        all_progress: List[UserProgress] = await self._progress_repository.get_all_for_user(
            user_id=user_id
        )
        completed_ids: set = set()
        for progress in all_progress:
            if progress.completed is True:
                completed_ids.add(progress.task_id)
        incomplete: List[Task] = []
        for task in all_tasks:
            if str(task.id) not in completed_ids:
                incomplete.append(task)
        return incomplete

    def _fill_time_budget(
        self, tasks: List[Task], budget_minutes: int
    ) -> List[Task]:
        """Select tasks that fit within the time budget in curriculum order.

        Tasks that are too large for the remaining budget are skipped (not
        used to stop the search). Only stops when remaining time falls below
        the minimum threshold or all tasks have been checked.

        Args:
            tasks (List[Task]): Incomplete tasks in preferred order.
            budget_minutes (int): Total available minutes after reservations.

        Returns:
            List[Task]: Selected tasks that fit within the budget.
        """
        selected: List[Task] = []
        remaining = budget_minutes
        for task in tasks:
            if remaining < _MIN_REMAINING_MINUTES:
                return selected
            if task.estimated_minutes <= remaining:
                selected.append(task)
                remaining -= task.estimated_minutes
        return selected

    def _to_task_items(self, tasks: List[Task]) -> List[SessionTaskItem]:
        """Convert Task documents to SessionTaskItem schemas.

        Args:
            tasks (List[Task]): Selected Task documents.

        Returns:
            List[SessionTaskItem]: Serialised task items for the response.
        """
        items: List[SessionTaskItem] = []
        for task in tasks:
            items.append(
                SessionTaskItem(
                    task_id=str(task.id),
                    slug=task.slug,
                    title=task.title,
                    task_type=task.task_type,
                    estimated_minutes=task.estimated_minutes,
                    xp_reward=task.xp_reward,
                )
            )
        return items
