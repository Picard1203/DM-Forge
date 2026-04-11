"""Abstract repository interface for the Spaced Repetition domain."""

from abc import abstractmethod
from typing import List, Optional

from src.models.review_card import SpacedRepCard, UserCardReview
from src.repositories.abstract.base_repository import AbstractBaseRepository


class AbstractReviewCardRepository(AbstractBaseRepository):
    """Abstract contract for spaced repetition card persistence operations."""

    @abstractmethod
    async def get_by_id(self, card_id: str) -> Optional[SpacedRepCard]:
        """Fetch a flashcard by its document ID.

        Args:
            card_id (str): String representation of the MongoDB ObjectId.

        Returns:
            Optional[SpacedRepCard]: The matching SpacedRepCard, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_due_cards(self, user_id: str, limit: int) -> List[UserCardReview]:
        """Fetch cards due for review by the given user.

        Args:
            user_id (str): The user's document ID.
            limit (int): Maximum number of due cards to return.

        Returns:
            List[UserCardReview]: List of UserCardReview documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_review_state(self, user_id: str, card_id: str) -> Optional[UserCardReview]:
        """Fetch the SM-2 review state for a specific user–card pair.

        Args:
            user_id (str): The user's document ID.
            card_id (str): The SpacedRepCard's document ID.

        Returns:
            Optional[UserCardReview]: The review state, or None if never reviewed.
        """
        raise NotImplementedError

    @abstractmethod
    async def save_review(self, review: UserCardReview) -> UserCardReview:
        """Create or update the SM-2 state for a user–card pair.

        Args:
            review (UserCardReview): The UserCardReview document to upsert.

        Returns:
            UserCardReview: The persisted or updated UserCardReview document.
        """
        raise NotImplementedError
