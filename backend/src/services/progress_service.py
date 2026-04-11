"""Progress service: task completion and module progress calculation."""

from typing import List, Optional

from src.models.progress import TaskCompletion, UserProgress
from src.repositories.abstract.progress_repository import AbstractProgressRepository
from src.repositories.abstract.task_repository import AbstractTaskRepository
from src.schemas.progress import CompleteTaskRequest, ModuleProgressResponse, ProgressOverviewResponse


class ProgressService:
    """Handles task completion events and progress aggregation.

    Attributes:
        _progress_repository: Injected repository for progress operations.
        _task_repository: Injected repository for task lookups.
    """

    def __init__(
        self,
        progress_repository: AbstractProgressRepository,
        task_repository: AbstractTaskRepository,
    ) -> None:
        """Initialise the service with progress and task repositories.

        Args:
            progress_repository: An AbstractProgressRepository implementation.
            task_repository: An AbstractTaskRepository implementation.
        """
        self._progress_repository = progress_repository
        self._task_repository = task_repository

    async def complete_task(self, user_id: str, request: CompleteTaskRequest) -> int:
        """Record a task completion and return the XP awarded.

        If the task has already been completed no XP is awarded and no
        duplicate record is inserted.

        Args:
            user_id: The ID of the user completing the task.
            request: The task and module IDs to record.

        Returns:
            XP awarded for this completion (0 if already completed).
        """
        already_done = await self._progress_repository.is_task_complete(
            user_id=user_id, task_id=request.task_id
        )
        if already_done is True:
            return 0

        task = await self._task_repository.get_by_id(request.task_id)
        xp_reward = 0 if task is None else task.xp_reward

        completion = TaskCompletion(
            user_id=user_id,
            task_id=request.task_id,
            module_id=request.module_id,
            xp_awarded=xp_reward,
        )
        await self._progress_repository.mark_task_complete(completion)
        await self._recalculate_module_progress(
            user_id=user_id, module_id=request.module_id
        )
        return xp_reward

    async def get_overview(self, user_id: str) -> ProgressOverviewResponse:
        """Build a full progress overview for a user across all modules.

        Args:
            user_id: The user's document ID.

        Returns:
            A ProgressOverviewResponse with per-module and aggregate stats.
        """
        all_progress: List[UserProgress] = await self._progress_repository.get_all_user_progress(
            user_id=user_id
        )
        total_completed = await self._progress_repository.count_user_completions(user_id=user_id)

        module_responses = [
            ModuleProgressResponse(
                module_id=p.module_id,
                tasks_completed=p.tasks_completed,
                tasks_total=p.tasks_total,
                percent_complete=p.percent_complete,
            )
            for p in all_progress
        ]

        return ProgressOverviewResponse(
            modules=module_responses,
            total_tasks_completed=total_completed,
            total_xp=0,  # TODO: sum from TaskCompletion in a future iteration
        )

    async def _recalculate_module_progress(self, user_id: str, module_id: str) -> None:
        """Recalculate and upsert the module-level progress summary.

        Args:
            user_id: The user's document ID.
            module_id: The module's document ID.
        """
        tasks = await self._task_repository.get_by_module(module_id=module_id)
        total = len(tasks)
        completed_count = 0
        for task in tasks:
            is_done = await self._progress_repository.is_task_complete(
                user_id=user_id, task_id=str(task.id)
            )
            if is_done is True:
                completed_count += 1

        percent = (completed_count / total * 100) if total > 0 else 0.0
        from datetime import datetime
        completed_at = datetime.utcnow() if completed_count == total and total > 0 else None

        progress = UserProgress(
            user_id=user_id,
            module_id=module_id,
            tasks_completed=completed_count,
            tasks_total=total,
            percent_complete=percent,
            completed_at=completed_at,
        )
        await self._progress_repository.upsert_module_progress(progress)
