"""Progress service: task completion and module progress calculation."""

from datetime import UTC, datetime
from typing import List

from src.models.curriculum import Module, Task
from src.models.progress import UserProgress
from src.models.user import User
from src.repositories.abstract.progress_repository import AbstractProgressRepository
from src.repositories.abstract.task_repository import AbstractTaskRepository
from src.schemas.achievement import AchievementResponse
from src.schemas.progress import (
    CompleteTaskResponse,
    ModuleProgressItem,
    ProgressOverviewResponse,
)
from src.services.achievement_service import AchievementService
from src.services.gamification_service import GamificationService
from src.utils.exceptions import TaskNotFoundError


class ProgressService:
    """Handles task completion events and progress aggregation.

    Attributes:
        _progress_repository (AbstractProgressRepository): Repository for progress.
        _task_repository (AbstractTaskRepository): Repository for tasks.
        _gamification_service (GamificationService): Service for XP and streak updates.
        _achievement_service (AchievementService): Service for achievement checks.
    """

    def __init__(
        self,
        progress_repository: AbstractProgressRepository,
        task_repository: AbstractTaskRepository,
        gamification_service: GamificationService,
        achievement_service: AchievementService,
    ) -> None:
        """Initialise the service with required dependencies.

        Args:
            progress_repository (AbstractProgressRepository): Progress repository.
            task_repository (AbstractTaskRepository): Task repository.
            gamification_service (GamificationService): Gamification service instance.
            achievement_service (AchievementService): Achievement service instance.
        """
        self._progress_repository = progress_repository
        self._task_repository = task_repository
        self._gamification_service = gamification_service
        self._achievement_service = achievement_service

    async def complete_task(
        self, user: User, task_id: str
    ) -> CompleteTaskResponse:
        """Record a task completion, award XP, update streak, and check achievements.

        Args:
            user (User): The authenticated user completing the task.
            task_id (str): ID of the task to mark as complete.

        Returns:
            CompleteTaskResponse: Result including XP earned and updated stats.

        Raises:
            TaskNotFoundError: If no task with that ID exists.
        """
        task: Task = await self._task_repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError()
        existing = await self._progress_repository.get_by_user_and_task(
            user_id=str(user.id), task_id=task_id
        )
        if existing is not None:
            return CompleteTaskResponse(
                already_completed=True,
                xp_earned=0,
                new_xp=user.xp,
                new_level=user.level,
                earned_achievements=[],
            )
        progress = UserProgress(
            user_id=str(user.id),
            task_id=task_id,
            module_id=task.module_id,
            completed=True,
            completed_at=datetime.now(UTC),
            xp_earned=task.xp_reward,
        )
        await self._progress_repository.create(progress)
        updated_user = await self._gamification_service.award_xp(user, task.xp_reward)
        updated_user = await self._gamification_service.update_streak(updated_user)
        earned_achievements = await self._check_task_achievements(
            user_id=str(user.id),
            module_id=task.module_id,
            updated_user=updated_user,
        )
        return CompleteTaskResponse(
            already_completed=False,
            xp_earned=task.xp_reward,
            new_xp=updated_user.xp,
            new_level=updated_user.level,
            earned_achievements=earned_achievements,
        )

    async def get_overview(
        self, user_id: str, all_modules: List[Module]
    ) -> ProgressOverviewResponse:
        """Build a full progress overview for a user across all modules.

        Args:
            user_id (str): The user's document ID.
            all_modules (List[Module]): All curriculum modules to include.

        Returns:
            ProgressOverviewResponse: Overview with per-module and aggregate stats.
        """
        all_progress = await self._progress_repository.get_all_for_user(user_id=user_id)
        module_items = await self._build_module_items(
            user_id=user_id, all_modules=all_modules, all_progress=all_progress
        )
        total_xp = self._sum_xp(all_progress)
        return ProgressOverviewResponse(modules=module_items, total_xp=total_xp)

    async def _check_task_achievements(
        self,
        user_id: str,
        module_id: str,
        updated_user: User,
    ) -> List[AchievementResponse]:
        """Check and award achievements triggered by a task completion event.

        Args:
            user_id (str): The user's document ID.
            module_id (str): The module the completed task belongs to.
            updated_user (User): The user after XP and streak updates.

        Returns:
            List[AchievementResponse]: All achievements newly earned.
        """
        earned: List[AchievementResponse] = []
        all_progress = await self._progress_repository.get_all_for_user(user_id=user_id)
        total_completed = self._count_all_completed(all_progress)
        task_earned = await self._achievement_service.check_and_award(
            user_id=user_id,
            event_type="tasks_completed",
            event_value=str(total_completed),
        )
        for item in task_earned:
            earned.append(item)
        streak_earned = await self._achievement_service.check_and_award(
            user_id=user_id,
            event_type="streak",
            event_value=str(updated_user.current_streak),
        )
        for item in streak_earned:
            earned.append(item)
        module_earned = await self._check_module_complete_achievements(
            user_id=user_id, module_id=module_id, all_progress=all_progress
        )
        for item in module_earned:
            earned.append(item)
        return earned

    async def _check_module_complete_achievements(
        self,
        user_id: str,
        module_id: str,
        all_progress: List[UserProgress],
    ) -> List[AchievementResponse]:
        """Check module-completion achievements when a task is finished.

        Calls check_and_award for the module slug if the module is now fully
        complete, and for the total count of completed modules.

        Args:
            user_id (str): The user's document ID.
            module_id (str): The module ID to check for completion.
            all_progress (List[UserProgress]): All progress records for the user.

        Returns:
            List[AchievementResponse]: Achievements newly earned from module completion.
        """
        earned: List[AchievementResponse] = []
        module_tasks = await self._task_repository.get_by_module_id(module_id=module_id)
        total_in_module = len(module_tasks)
        completed_in_module = self._count_completed_in_module(
            module_id=module_id, all_progress=all_progress
        )
        if total_in_module > 0 and completed_in_module >= total_in_module:
            slug_earned = await self._achievement_service.check_and_award(
                user_id=user_id,
                event_type="module_complete",
                event_value=module_id,
            )
            for item in slug_earned:
                earned.append(item)
            completed_module_ids = self._get_completed_module_ids(all_progress)
            count_earned = await self._achievement_service.check_and_award(
                user_id=user_id,
                event_type="module_complete",
                event_value=str(len(completed_module_ids)),
            )
            for item in count_earned:
                earned.append(item)
        return earned

    async def _build_module_items(
        self,
        user_id: str,
        all_modules: List[Module],
        all_progress: List[UserProgress],
    ) -> List[ModuleProgressItem]:
        """Build a ModuleProgressItem for each module.

        Args:
            user_id (str): The user's document ID.
            all_modules (List[Module]): All curriculum modules.
            all_progress (List[UserProgress]): All progress records for the user.

        Returns:
            List[ModuleProgressItem]: One item per module with completion stats.
        """
        module_items: List[ModuleProgressItem] = []
        for module in all_modules:
            module_id = str(module.id)
            completed_count = self._count_completed_in_module(
                module_id=module_id, all_progress=all_progress
            )
            tasks = await self._task_repository.get_by_module_id(module_id=module_id)
            total = len(tasks)
            percent = (completed_count / total * 100.0) if total > 0 else 0.0
            module_items.append(
                ModuleProgressItem(
                    module_id=module_id,
                    completed=completed_count,
                    total=total,
                    percent=percent,
                )
            )
        return module_items

    def _count_completed_in_module(
        self, module_id: str, all_progress: List[UserProgress]
    ) -> int:
        """Count completed task records belonging to a specific module.

        Args:
            module_id (str): The module's document ID.
            all_progress (List[UserProgress]): All progress records for the user.

        Returns:
            int: Number of completed task records for the module.
        """
        count = 0
        for progress in all_progress:
            if progress.module_id == module_id and progress.completed is True:
                count += 1
        return count

    def _count_all_completed(self, all_progress: List[UserProgress]) -> int:
        """Count all completed task records across all modules.

        Args:
            all_progress (List[UserProgress]): All progress records for the user.

        Returns:
            int: Total number of completed task records.
        """
        count = 0
        for progress in all_progress:
            if progress.completed is True:
                count += 1
        return count

    def _get_completed_module_ids(self, all_progress: List[UserProgress]) -> set:
        """Collect unique module IDs that have at least one completed task.

        Args:
            all_progress (List[UserProgress]): All progress records for the user.

        Returns:
            set: Set of module_id strings with at least one completion.
        """
        module_ids: set = set()
        for progress in all_progress:
            if progress.completed is True:
                module_ids.add(progress.module_id)
        return module_ids

    def _sum_xp(self, all_progress: List[UserProgress]) -> int:
        """Sum the XP earned across all completed progress records.

        Args:
            all_progress (List[UserProgress]): All progress records for the user.

        Returns:
            int: Total XP earned from completed tasks.
        """
        total = 0
        for progress in all_progress:
            total += progress.xp_earned
        return total
