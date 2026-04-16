"""MongoDB implementation of the AbstractReviewCardRepository."""

from datetime import UTC, datetime
from typing import List, Optional

from beanie import PydanticObjectId

from src.models.review_card import ReviewCard, UserCardReview
from src.repositories.abstract.review_card_repository import AbstractReviewCardRepository


class MongoReviewCardRepository(AbstractReviewCardRepository):
    """Concrete MongoDB repository for spaced repetition using Beanie ODM."""

    async def get_card_by_id(self, card_id: str) -> Optional[ReviewCard]:
        """Fetch a review card by its document ID.

        Args:
            card_id (str): String representation of the MongoDB ObjectId.

        Returns:
            Optional[ReviewCard]: The matching ReviewCard, or None if not found.
        """
        return await ReviewCard.get(PydanticObjectId(card_id))

    async def get_all_cards(self) -> List[ReviewCard]:
        """Fetch all review cards across all modules.

        Returns:
            List[ReviewCard]: All ReviewCard documents.
        """
        return await ReviewCard.find_all().to_list()

    async def get_due_cards(self, user_id: str) -> List[ReviewCard]:
        """Fetch cards due for review by the given user.

        Returns cards whose next_review timestamp is in the past, plus any
        cards the user has never reviewed.

        Args:
            user_id (str): The user's document ID.

        Returns:
            List[ReviewCard]: ReviewCard documents due for review.
        """
        all_cards = await ReviewCard.find_all().to_list()
        now = datetime.now(UTC)
        all_reviews = await UserCardReview.find(
            UserCardReview.user_id == user_id
        ).to_list()
        reviewed_map = {}
        for review in all_reviews:
            reviewed_map[review.card_id] = review
        due_cards: List[ReviewCard] = []
        for card in all_cards:
            card_id = str(card.id)
            if card_id not in reviewed_map:
                due_cards.append(card)
            else:
                card_next_review = reviewed_map[card_id].next_review
                if card_next_review.tzinfo is None:
                    card_next_review = card_next_review.replace(tzinfo=UTC)
                if card_next_review <= now:
                    due_cards.append(card)
        return due_cards

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
        existing = await self.get_review_record(
            user_id=review.user_id,
            card_id=review.card_id,
        )
        if existing is not None:
            existing.ease_factor = review.ease_factor
            existing.interval_days = review.interval_days
            existing.repetitions = review.repetitions
            existing.next_review = review.next_review
            existing.last_reviewed = review.last_reviewed
            await existing.save()
            return existing
        await review.insert()
        return review
