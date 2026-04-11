"""Abstract repository interface for the Task domain."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.curriculum import Task


class AbstractTaskRepository(ABC):
    """Abstract contract for task data persistence operations."""

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Fetch a task by its document ID.

        Args:
            task_id (str): String representation of the MongoDB ObjectId.

        Returns:
            Optional[Task]: The matching Task document, or None if not found.

        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Task]:
        """Fetch a task by its URL slug.

        Args:
            slug (str): The URL-safe slug to search for.

        Returns:
            Optional[Task]: The matching Task document, or None if not found.

        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_module(self, module_id: str) -> List[Task]:
        """Fetch all tasks belonging to a module, ordered by order ascending.

        Args:
            module_id (str): The parent module's document ID.

        Returns:
            List[Task]: Ordered list of Task documents.

        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Persist a new task document.

        Args:
            task (Task): The Task instance to insert.

        Returns:
            Task: The persisted Task document with its assigned ID.

        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Persist changes to an existing task document.

        Args:
            task (Task): The Task instance with updated fields.

        Returns:
            Task: The updated Task document.

        """
        raise NotImplementedError
