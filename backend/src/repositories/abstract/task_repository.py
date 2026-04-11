"""Abstract interface for Task repository operations."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.curriculum import Task


class AbstractTaskRepository(ABC):
    """Contract for all Task repository implementations."""

    @abstractmethod
    async def get_by_module_id(self, module_id: str) -> List[Task]:
        """Retrieve all tasks belonging to a module, sorted by order ascending.

        Args:
            module_id (str): The parent module's document ID string.

        Returns:
            (List[Task]): Ordered list of Task documents for the given module.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Task]:
        """Retrieve a single task by its URL slug.

        Args:
            slug (str): The URL-safe slug to search for.

        Returns:
            (Optional[Task]): The matching Task document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a single task by its document ID.

        Args:
            task_id (str): String representation of the MongoDB ObjectId.

        Returns:
            (Optional[Task]): The matching Task document, or None if not found.
        """
        raise NotImplementedError
