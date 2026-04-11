"""Abstract repository interface for the Task domain."""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.curriculum import Task


class AbstractTaskRepository(ABC):
    """Abstract contract for task data persistence operations."""

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Fetch a task by its document ID.

        Args:
            task_id: String representation of the MongoDB ObjectId.

        Returns:
            The matching Task document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Task]:
        """Fetch a task by its URL slug.

        Args:
            slug: The URL-safe slug to search for.

        Returns:
            The matching Task document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_module(self, module_id: str) -> List[Task]:
        """Fetch all tasks belonging to a module, ordered by ``order`` ascending.

        Args:
            module_id: The parent module's document ID.

        Returns:
            Ordered list of Task documents for the given module.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Persist a new task document.

        Args:
            task: The Task instance to insert.

        Returns:
            The persisted Task document with its assigned ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Persist changes to an existing task document.

        Args:
            task: The Task instance with updated fields.

        Returns:
            The updated Task document.
        """
        raise NotImplementedError
