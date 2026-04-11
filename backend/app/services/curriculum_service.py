"""Curriculum service: module and task retrieval with ordering logic."""

from typing import List, Optional

from app.models.curriculum import Module, Task
from app.repositories.abstract.module_repository import AbstractModuleRepository
from app.repositories.abstract.task_repository import AbstractTaskRepository
from app.utils.exceptions import ResourceNotFoundError


class CurriculumService:
    """Handles retrieval and ordering of curriculum content.

    Attributes:
        _module_repository: Injected repository for module operations.
        _task_repository: Injected repository for task operations.
    """

    def __init__(
        self,
        module_repository: AbstractModuleRepository,
        task_repository: AbstractTaskRepository,
    ) -> None:
        """Initialise the service with module and task repositories.

        Args:
            module_repository: An AbstractModuleRepository implementation.
            task_repository: An AbstractTaskRepository implementation.
        """
        self._module_repository = module_repository
        self._task_repository = task_repository

    async def list_modules(self) -> List[Module]:
        """Return all modules ordered by their ``order`` field.

        Returns:
            Ordered list of Module documents.
        """
        return await self._module_repository.get_ordered()

    async def get_module(self, module_id: str) -> Module:
        """Fetch a single module by ID.

        Args:
            module_id: The module's document ID.

        Returns:
            The matching Module document.

        Raises:
            ResourceNotFoundError: If no module with that ID exists.
        """
        module: Optional[Module] = await self._module_repository.get_by_id(module_id)
        if module is None:
            raise ResourceNotFoundError("Module")
        return module

    async def get_module_tasks(self, module_id: str) -> List[Task]:
        """Fetch all tasks for a module, ordered by ``order`` ascending.

        Args:
            module_id: The parent module's document ID.

        Returns:
            Ordered list of Task documents.
        """
        return await self._task_repository.get_by_module(module_id)

    async def get_task(self, task_id: str) -> Task:
        """Fetch a single task by ID.

        Args:
            task_id: The task's document ID.

        Returns:
            The matching Task document.

        Raises:
            ResourceNotFoundError: If no task with that ID exists.
        """
        task: Optional[Task] = await self._task_repository.get_by_id(task_id)
        if task is None:
            raise ResourceNotFoundError("Task")
        return task
