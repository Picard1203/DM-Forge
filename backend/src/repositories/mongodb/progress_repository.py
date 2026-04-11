"""MongoDB implementation of the AbstractProgressRepository."""

from typing import List, Optional

from src.models.progress import TaskCompletion, UserProgress
from src.repositories.abstract.progress_repository import AbstractProgressRepository


class MongoProgressRepository(AbstractProgressRepository):
    """Concrete MongoDB repository for progress tracking using Beanie ODM."""

    async def get_user_progress(self, user_id: str, module_id: str) -> Optional[UserProgress]:
        """Fetch a user's progress record for a specific module.

        Args:
            user_id: The user's document ID.
            module_id: The module's document ID.

        Returns:
            The UserProgress document, or None if the user has not started.
        """
        return await UserProgress.find_one(
            UserProgress.user_id == user_id,
            UserProgress.module_id == module_id,
        )

    async def get_all_user_progress(self, user_id: str) -> List[UserProgress]:
        """Fetch all progress records for a user across all modules.

        Args:
            user_id: The user's document ID.

        Returns:
            List of UserProgress documents for the given user.
        """
        return await UserProgress.find(UserProgress.user_id == user_id).to_list()

    async def mark_task_complete(self, completion: TaskCompletion) -> TaskCompletion:
        """Persist a task completion event.

        Args:
            completion: The TaskCompletion document to insert.

        Returns:
            The persisted TaskCompletion with its assigned ID.
        """
        await completion.insert()
        return completion

    async def is_task_complete(self, user_id: str, task_id: str) -> bool:
        """Check whether a specific task has already been completed by a user.

        Args:
            user_id: The user's document ID.
            task_id: The task's document ID.

        Returns:
            True if a completion record exists, False otherwise.
        """
        existing = await TaskCompletion.find_one(
            TaskCompletion.user_id == user_id,
            TaskCompletion.task_id == task_id,
        )
        return existing is not None

    async def upsert_module_progress(self, progress: UserProgress) -> UserProgress:
        """Create or update the module-level progress summary.

        Args:
            progress: The UserProgress document to upsert.

        Returns:
            The persisted or updated UserProgress document.
        """
        existing = await self.get_user_progress(
            user_id=progress.user_id,
            module_id=progress.module_id,
        )
        if existing is not None:
            existing.tasks_completed = progress.tasks_completed
            existing.tasks_total = progress.tasks_total
            existing.percent_complete = progress.percent_complete
            existing.completed_at = progress.completed_at
            await existing.save()
            return existing
        await progress.insert()
        return progress

    async def count_user_completions(self, user_id: str) -> int:
        """Count the total number of task completions for a user.

        Args:
            user_id: The user's document ID.

        Returns:
            Total task completion count.
        """
        return await TaskCompletion.find(TaskCompletion.user_id == user_id).count()
