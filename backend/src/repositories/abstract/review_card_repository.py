"""Abstract repository interface for the Spaced Repetition domain."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.review_card import ReviewCard, UserCardReview


class AbstractReviewCardRepository(ABC):
    """Abstract contract for spaced repetition card persistence operations."""

    @abstractmethod
    async def get_card_by_id(self, card_id: str) -> Optional[ReviewCard]:
        """Fetch a review card by its document ID.

        Args:
            card_id (str): String representation of the MongoDB ObjectId.

        Returns:
            Optional[ReviewCard]: The matching ReviewCard, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_cards(self) -> List[ReviewCard]:
        """Fetch all review cards across all modules.

        Returns:
            List[ReviewCard]: All ReviewCard documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_due_cards(self, user_id: str) -> List[ReviewCard]:
        """Fetch cards due for review by the given user.

        Returns cards whose scheduled next_review is in the past, plus any
        cards the user has never reviewed at all.

        Args:
            user_id (str): The user's document ID.

        Returns:
            List[ReviewCard]: ReviewCard documents due for review.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_review_record(
        self, user_id: str, card_id: str
    ) -> Optional[UserCardReview]:
        """Fetch the SM-2 review state for a specific user–card pair.

        Args:
            user_id (str): The user's document ID.
            card_id (str): The ReviewCard's document ID.

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
