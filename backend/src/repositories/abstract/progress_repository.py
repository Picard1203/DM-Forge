"""Abstract repository interface for the Progress domain."""

from abc import abstractmethod
from typing import List, Optional

from src.models.progress import TaskCompletion, UserProgress
from src.repositories.abstract.base_repository import AbstractBaseRepository


class AbstractProgressRepository(AbstractBaseRepository):
    """Abstract contract for progress data persistence operations."""

    @abstractmethod
    async def get_user_progress(self, user_id: str, module_id: str) -> Optional[UserProgress]:
        """Fetch a user's progress record for a specific module.

        Args:
            user_id (str): The user's document ID.
            module_id (str): The module's document ID.

        Returns:
            Optional[UserProgress]: Progress document, or None if not started.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_user_progress(self, user_id: str) -> List[UserProgress]:
        """Fetch all progress records for a user across all modules.

        Args:
            user_id (str): The user's document ID.

        Returns:
            List[UserProgress]: List of UserProgress documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def mark_task_complete(self, completion: TaskCompletion) -> TaskCompletion:
        """Persist a task completion event.

        Args:
            completion (TaskCompletion): The document to insert.

        Returns:
            TaskCompletion: The persisted TaskCompletion document.
        """
        raise NotImplementedError

    @abstractmethod
    async def is_task_complete(self, user_id: str, task_id: str) -> bool:
        """Check whether a specific task has already been completed.

        Args:
            user_id (str): The user's document ID.
            task_id (str): The task's document ID.

        Returns:
            bool: True if a completion record exists, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def upsert_module_progress(self, progress: UserProgress) -> UserProgress:
        """Create or update the module-level progress summary.

        Args:
            progress (UserProgress): The UserProgress document to upsert.

        Returns:
            UserProgress: The persisted or updated UserProgress document.
        """
        raise NotImplementedError

    @abstractmethod
    async def count_user_completions(self, user_id: str) -> int:
        """Count the total number of task completions for a user.

        Args:
            user_id (str): The user's document ID.

        Returns:
            int: Total task completion count.
        """
        raise NotImplementedError
