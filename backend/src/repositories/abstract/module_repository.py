"""Abstract interface for Module repository operations."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.curriculum import Module


class AbstractModuleRepository(ABC):
    """Contract for all Module repository implementations."""

    @abstractmethod
    async def get_all(self) -> List[Module]:
        """Retrieve all modules sorted by display order.

        Returns:
        List[Module]: All Module documents ordered by their order field ascending.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Module]:
        """Retrieve a single module by its URL slug.

        Args:
            slug (str): The URL-safe slug to search for.

        Returns:
        Optional[Module]: The matching Module document, or None if not found.
        """
        raise NotImplementedError
