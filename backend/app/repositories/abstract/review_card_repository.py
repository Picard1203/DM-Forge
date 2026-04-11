"""Abstract repository interface for the Spaced Repetition domain."""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.review_card import SpacedRepCard, UserCardReview


class AbstractReviewCardRepository(ABC):
    """Abstract contract for spaced repetition card persistence operations."""

    @abstractmethod
    async def get_by_id(self, card_id: str) -> Optional[SpacedRepCard]:
        """Fetch a flashcard by its document ID.

        Args:
            card_id: String representation of the MongoDB ObjectId.

        Returns:
            The matching SpacedRepCard, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_due_cards(self, user_id: str, limit: int) -> List[UserCardReview]:
        """Fetch cards due for review by the given user.

        Args:
            user_id: The user's document ID.
            limit: Maximum number of due cards to return.

        Returns:
            List of UserCardReview documents with ``next_review_at`` in the past.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_review_state(self, user_id: str, card_id: str) -> Optional[UserCardReview]:
        """Fetch the SM-2 review state for a specific user–card pair.

        Args:
            user_id: The user's document ID.
            card_id: The SpacedRepCard's document ID.

        Returns:
            The UserCardReview document, or None if the card has never been reviewed.
        """
        raise NotImplementedError

    @abstractmethod
    async def save_review(self, review: UserCardReview) -> UserCardReview:
        """Create or update the SM-2 state for a user–card pair.

        Args:
            review: The UserCardReview document to upsert.

        Returns:
            The persisted or updated UserCardReview document.
        """
        raise NotImplementedError
