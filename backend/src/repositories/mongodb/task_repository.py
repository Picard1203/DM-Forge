"""MongoDB implementation of the AbstractTaskRepository."""

from typing import List, Optional

from beanie import PydanticObjectId

from src.models.curriculum import Task
from src.repositories.abstract.task_repository import AbstractTaskRepository


class MongoTaskRepository(AbstractTaskRepository):
    """Concrete MongoDB repository for Task documents using Beanie ODM."""

    async def get_by_module_id(self, module_id: str) -> List[Task]:
        """Retrieve all tasks for a module, sorted by order ascending.

        Args:
            module_id (str): The parent module's document ID string.

        Returns:
        List[Task]: Ordered list of Task documents for the given module.
        """
        return await Task.find(Task.module_id == module_id).sort("+order").to_list()

    async def get_by_slug(self, slug: str) -> Optional[Task]:
        """Retrieve a single task by its URL slug.

        Args:
            slug (str): The URL-safe slug to search for.

        Returns:
        Optional[Task]: The matching Task document, or None if not found.
        """
        return await Task.find_one(Task.slug == slug)

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a single task by its document ID.

        Args:
            task_id (str): String representation of the MongoDB ObjectId.

        Returns:
        Optional[Task]: The matching Task document, or None if not found.
        """
        return await Task.get(PydanticObjectId(task_id))
