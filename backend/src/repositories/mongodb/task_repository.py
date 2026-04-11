"""MongoDB implementation of the AbstractTaskRepository."""

from typing import List, Optional

from beanie import PydanticObjectId

from src.models.curriculum import Task
from src.repositories.abstract.task_repository import AbstractTaskRepository


class MongoTaskRepository(AbstractTaskRepository):
    """Concrete MongoDB repository for Task documents using Beanie ODM."""

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Fetch a task by its document ID.

        Args:
            task_id: String representation of the MongoDB ObjectId.

        Returns:
            The matching Task document, or None if not found.
        """
        return await Task.get(PydanticObjectId(task_id))

    async def get_by_slug(self, slug: str) -> Optional[Task]:
        """Fetch a task by its URL slug.

        Args:
            slug: The URL-safe slug to search for.

        Returns:
            The matching Task document, or None if not found.
        """
        return await Task.find_one(Task.slug == slug)

    async def get_by_module(self, module_id: str) -> List[Task]:
        """Fetch all tasks for a module, ordered by ``order`` ascending.

        Args:
            module_id: The parent module's document ID.

        Returns:
            Ordered list of Task documents.
        """
        return await Task.find(Task.module_id == module_id).sort(+Task.order).to_list()

    async def create(self, task: Task) -> Task:
        """Persist a new task document.

        Args:
            task: The Task instance to insert.

        Returns:
            The persisted Task document with its assigned ID.
        """
        await task.insert()
        return task

    async def update(self, task: Task) -> Task:
        """Persist changes to an existing task document.

        Args:
            task: The Task instance with updated fields.

        Returns:
            The updated Task document.
        """
        await task.save()
        return task
