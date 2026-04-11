"""Curriculum service: module and task retrieval with ordering logic."""

from typing import List, Optional

from src.models.curriculum import Module, Task
from src.repositories.abstract.module_repository import AbstractModuleRepository
from src.repositories.abstract.task_repository import AbstractTaskRepository
from src.utils.exceptions import ModuleNotFoundError


class CurriculumService:
    """Handles retrieval and ordering of curriculum content.

    Attributes:
        _module_repository (AbstractModuleRepository): Repository for modules.
        _task_repository (AbstractTaskRepository): Repository for tasks.
    """

    def __init__(
        self,
        module_repository: AbstractModuleRepository,
        task_repository: AbstractTaskRepository,
    ) -> None:
        """Initialise the service with module and task repositories.

        Args:
            module_repository (AbstractModuleRepository): Module repository.
            task_repository (AbstractTaskRepository): Task repository.
        """
        self._module_repository = module_repository
        self._task_repository = task_repository

    async def get_all_modules(self) -> List[Module]:
        """Return all modules ordered by their order field ascending.

        Returns:
        List[Module]: Ordered list of Module documents.
        """
        return await self._module_repository.get_all()

    async def get_module_by_slug(self, slug: str) -> Module:
        """Fetch a single module by its URL slug.

        Args:
            slug (str): The URL-safe slug to search for.

        Returns:
            (Module): The matching Module document.

        Raises:
            ModuleNotFoundError: If no module with that slug exists.
        """
        module: Optional[Module] = await self._module_repository.get_by_slug(slug)
        if module is None:
            raise ModuleNotFoundError()
        return module

    async def get_tasks_for_module(self, slug: str) -> List[Task]:
        """Fetch all tasks for a module identified by slug, ordered by order ascending.

        Args:
            slug (str): The URL-safe slug of the parent module.

        Returns:
        List[Task]: Ordered list of Task documents for the module.

        Raises:
            ModuleNotFoundError: If no module with that slug exists.
        """
        module: Optional[Module] = await self._module_repository.get_by_slug(slug)
        if module is None:
            raise ModuleNotFoundError()
        return await self._task_repository.get_by_module_id(str(module.id))
