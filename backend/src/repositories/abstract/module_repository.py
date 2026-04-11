"""Abstract repository interface for the Module domain."""

from abc import abstractmethod
from typing import List, Optional

from src.models.curriculum import Module
from src.repositories.abstract.base_repository import AbstractBaseRepository


class AbstractModuleRepository(AbstractBaseRepository):
    """Abstract contract for module data persistence operations."""

    @abstractmethod
    async def get_all(self) -> List[Module]:
        """Fetch all modules, unordered.

        Returns:
            List[Module]: List of all Module documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_ordered(self) -> List[Module]:
        """Fetch all modules sorted by order ascending.

        Returns:
            List[Module]: Ordered list of Module documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, module_id: str) -> Optional[Module]:
        """Fetch a module by its document ID.

        Args:
            module_id (str): String representation of the MongoDB ObjectId.

        Returns:
            Optional[Module]: The matching Module document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Module]:
        """Fetch a module by its URL slug.

        Args:
            slug (str): The URL-safe slug to search for.

        Returns:
            Optional[Module]: The matching Module document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, module: Module) -> Module:
        """Persist a new module document.

        Args:
            module (Module): The Module instance to insert.

        Returns:
            Module: The persisted Module document with its assigned ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, module: Module) -> Module:
        """Persist changes to an existing module document.

        Args:
            module (Module): The Module instance with updated fields.

        Returns:
            Module: The updated Module document.
        """
        raise NotImplementedError
