"""Abstract repository interface for the Progress domain."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.progress import TaskCompletion, UserProgress


class AbstractProgressRepository(ABC):
    """Abstract contract for user progress persistence operations."""

    @abstractmethod
    async def get_user_progress(self, user_id: str, module_id: str) -> Optional[UserProgress]:
        """Fetch a user's progress record for a specific module.

        Args:
            user_id: The user's document ID.
            module_id: The module's document ID.

        Returns:
            The UserProgress document, or None if the user has not started.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_user_progress(self, user_id: str) -> List[UserProgress]:
        """Fetch all progress records for a user across all modules.

        Args:
            user_id: The user's document ID.

        Returns:
            List of UserProgress documents for the given user.
        """
        raise NotImplementedError

    @abstractmethod
    async def mark_task_complete(self, completion: TaskCompletion) -> TaskCompletion:
        """Persist a task completion event.

        Args:
            completion: The TaskCompletion document to insert.

        Returns:
            The persisted TaskCompletion document with its assigned ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def is_task_complete(self, user_id: str, task_id: str) -> bool:
        """Check whether a specific task has already been completed by a user.

        Args:
            user_id: The user's document ID.
            task_id: The task's document ID.

        Returns:
            True if a completion record exists, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def upsert_module_progress(self, progress: UserProgress) -> UserProgress:
        """Create or update the module-level progress summary.

        Args:
            progress: The UserProgress document to upsert.

        Returns:
            The persisted or updated UserProgress document.
        """
        raise NotImplementedError

    @abstractmethod
    async def count_user_completions(self, user_id: str) -> int:
        """Count the total number of task completions for a user.

        Args:
            user_id: The user's document ID.

        Returns:
            Total task completion count.
        """
        raise NotImplementedError
