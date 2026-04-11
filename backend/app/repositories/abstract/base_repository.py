"""Abstract base repository defining generic CRUD operations."""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class AbstractBaseRepository(ABC, Generic[T]):
    """Generic abstract repository for common CRUD operations.

    Subclasses should bind the TypeVar ``T`` to a specific Beanie Document
    type and implement all abstract methods against a real data store.
    """

    @abstractmethod
    async def get_by_id(self, document_id: str) -> Optional[T]:
        """Fetch a single document by its ID.

        Args:
            document_id: The string representation of the MongoDB ObjectId.

        Returns:
            The matching document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, document: T) -> T:
        """Persist a new document to the data store.

        Args:
            document: The document instance to insert.

        Returns:
            The persisted document with its assigned ID populated.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, document: T) -> T:
        """Update an existing document in the data store.

        Args:
            document: The document instance with updated fields.

        Returns:
            The updated document.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, document_id: str) -> None:
        """Delete a document from the data store.

        Args:
            document_id: The string representation of the MongoDB ObjectId.
        """
        raise NotImplementedError
