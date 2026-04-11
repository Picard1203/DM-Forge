"""MongoDB implementation of the AbstractModuleRepository."""

from typing import List, Optional

from beanie import PydanticObjectId

from app.models.curriculum import Module
from app.repositories.abstract.module_repository import AbstractModuleRepository


class MongoModuleRepository(AbstractModuleRepository):
    """Concrete MongoDB repository for Module documents using Beanie ODM."""

    async def get_all(self) -> List[Module]:
        """Fetch all modules, unordered.

        Returns:
            List of all Module documents.
        """
        return await Module.find_all().to_list()

    async def get_ordered(self) -> List[Module]:
        """Fetch all modules sorted by ``order`` ascending.

        Returns:
            Ordered list of Module documents.
        """
        return await Module.find_all().sort(+Module.order).to_list()

    async def get_by_id(self, module_id: str) -> Optional[Module]:
        """Fetch a module by its document ID.

        Args:
            module_id: String representation of the MongoDB ObjectId.

        Returns:
            The matching Module document, or None if not found.
        """
        return await Module.get(PydanticObjectId(module_id))

    async def get_by_slug(self, slug: str) -> Optional[Module]:
        """Fetch a module by its URL slug.

        Args:
            slug: The URL-safe slug to search for.

        Returns:
            The matching Module document, or None if not found.
        """
        return await Module.find_one(Module.slug == slug)

    async def create(self, module: Module) -> Module:
        """Persist a new module document.

        Args:
            module: The Module instance to insert.

        Returns:
            The persisted Module document with its assigned ID.
        """
        await module.insert()
        return module

    async def update(self, module: Module) -> Module:
        """Persist changes to an existing module document.

        Args:
            module: The Module instance with updated fields.

        Returns:
            The updated Module document.
        """
        await module.save()
        return module
