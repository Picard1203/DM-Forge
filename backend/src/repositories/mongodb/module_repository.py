"""MongoDB implementation of the AbstractModuleRepository."""

from typing import List, Optional

from src.models.curriculum import Module
from src.repositories.abstract.module_repository import AbstractModuleRepository


class MongoModuleRepository(AbstractModuleRepository):
    """Concrete MongoDB repository for Module documents using Beanie ODM."""

    async def get_all(self) -> List[Module]:
        """Retrieve all modules sorted by display order ascending.

        Returns:
            (List[Module]): All Module documents ordered by their order field.
        """
        return await Module.find_all().sort("+order").to_list()

    async def get_by_slug(self, slug: str) -> Optional[Module]:
        """Retrieve a single module by its URL slug.

        Args:
            slug (str): The URL-safe slug to search for.

        Returns:
            (Optional[Module]): The matching Module document, or None if not found.
        """
        return await Module.find_one(Module.slug == slug)
