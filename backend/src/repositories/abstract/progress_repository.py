"""Abstract repository interface for the Progress domain."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.progress import UserProgress


class AbstractProgressRepository(ABC):
    """Abstract contract for progress data persistence operations."""

    @abstractmethod
    async def get_by_user_and_task(
        self, user_id: str, task_id: str
    ) -> Optional[UserProgress]:
        """Fetch the progress record for a specific user-task pair.

        Args:
            user_id (str): The user's document ID.
            task_id (str): The task's document ID.

        Returns:
            Optional[UserProgress]: The matching document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_and_module(
        self, user_id: str, module_id: str
    ) -> List[UserProgress]:
        """Fetch all progress records for a user within a specific module.

        Args:
            user_id (str): The user's document ID.
            module_id (str): The module's document ID.

        Returns:
            List[UserProgress]: All UserProgress documents for that module.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_for_user(self, user_id: str) -> List[UserProgress]:
        """Fetch every progress record belonging to a user across all modules.

        Args:
            user_id (str): The user's document ID.

        Returns:
            List[UserProgress]: All UserProgress documents for the user.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, progress: UserProgress) -> UserProgress:
        """Persist a new UserProgress document.

        Args:
            progress (UserProgress): The document instance to insert.

        Returns:
            UserProgress: The persisted document with its assigned ID.
        """
        raise NotImplementedError
