"""MongoDB implementation of the AbstractReviewCardRepository."""

from datetime import UTC, datetime
from typing import List, Optional

from beanie import PydanticObjectId

from src.models.review_card import SpacedRepCard, UserCardReview
from src.repositories.abstract.review_card_repository import AbstractReviewCardRepository


class MongoReviewCardRepository(AbstractReviewCardRepository):
    """Concrete MongoDB repository for spaced repetition using Beanie ODM."""

    async def get_by_id(self, card_id: str) -> Optional[SpacedRepCard]:
        """Fetch a flashcard by its document ID.

        Args:
            card_id (str): String representation of the MongoDB ObjectId.

        Returns:
            Optional[SpacedRepCard]: The matching SpacedRepCard, or None if not found.
        """
        return await SpacedRepCard.get(PydanticObjectId(card_id))

    async def get_due_cards(self, user_id: str, limit: int) -> List[UserCardReview]:
        """Fetch cards due for review by the given user.

        Args:
            user_id (str): The user's document ID.
            limit (int): Maximum number of due cards to return.

        Returns:
            List[UserCardReview]: List of UserCardReview documents.
        """
        now = datetime.now(UTC)
        return await UserCardReview.find(
            UserCardReview.user_id == user_id,
            UserCardReview.next_review_at <= now,
        ).limit(limit).to_list()

    async def get_review_state(self, user_id: str, card_id: str) -> Optional[UserCardReview]:
        """Fetch the SM-2 review state for a specific user–card pair.

        Args:
            user_id (str): The user's document ID.
            card_id (str): The SpacedRepCard's document ID.

        Returns:
            Optional[UserCardReview]: The review state, or None if never reviewed.
        """
        return await UserCardReview.find_one(
            UserCardReview.user_id == user_id,
            UserCardReview.card_id == card_id,
        )

    async def save_review(self, review: UserCardReview) -> UserCardReview:
        """Create or update the SM-2 state for a user–card pair.

        Args:
            review (UserCardReview): The UserCardReview document to upsert.

        Returns:
            UserCardReview: The persisted or updated UserCardReview document.
        """
        existing = await self.get_review_state(
            user_id=review.user_id,
            card_id=review.card_id,
        )
        if existing is not None:
            existing.easiness_factor = review.easiness_factor
            existing.interval_days = review.interval_days
            existing.repetitions = review.repetitions
            existing.next_review_at = review.next_review_at
            existing.last_reviewed_at = review.last_reviewed_at
            await existing.save()
            return existing
        await review.insert()
        return review
