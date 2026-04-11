"""Abstract base repository defining core interface contract."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class AbstractBaseRepository(ABC):
    """Abstract interface for standard repository operations."""

    @abstractmethod
    async def get_by_id(self, document_id: str) -> Optional[Any]:
        """Fetch a single document by its ID.

        Args:
            document_id (str): The string representation of the MongoDB ObjectId.

        Returns:
            Optional[Any]: The matching document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, document: Any) -> Any:
        """Persist a new document to the data store.

        Args:
            document (Any): The document instance to insert.

        Returns:
            Any: The persisted document with its assigned ID populated.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, document: Any) -> Any:
        """Update an existing document in the data store.

        Args:
            document (Any): The document instance with updated fields.

        Returns:
            Any: The updated document.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, document_id: str) -> None:
        """Delete a document from the data store.

        Args:
            document_id (str): The string representation of the MongoDB ObjectId.
        """
        raise NotImplementedError
