"""Review service: spaced repetition scheduling using the SM-2 algorithm."""

from datetime import datetime, timedelta
from typing import List, Optional

from app.models.review_card import SpacedRepCard, UserCardReview
from app.repositories.abstract.review_card_repository import AbstractReviewCardRepository
from app.schemas.review import CardReviewResponse, ReviewSubmitRequest, ReviewSubmitResponse
from app.utils.exceptions import ResourceNotFoundError


def _apply_sm2(review: UserCardReview, quality: int) -> UserCardReview:
    """Apply the SM-2 algorithm to update a card's scheduling state.

    Args:
        review: The current UserCardReview state.
        quality: Response quality from 0 (complete blackout) to 5 (perfect).

    Returns:
        The updated UserCardReview with new interval, repetitions, and EF.
    """
    if quality < 3:
        review.repetitions = 0
        review.interval_days = 1
    else:
        if review.repetitions == 0:
            review.interval_days = 1
        elif review.repetitions == 1:
            review.interval_days = 6
        else:
            review.interval_days = round(review.interval_days * review.easiness_factor)
        review.repetitions += 1

    new_ef = review.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    review.easiness_factor = max(1.3, new_ef)
    review.next_review_at = datetime.utcnow() + timedelta(days=review.interval_days)
    review.last_reviewed_at = datetime.utcnow()
    return review


class ReviewService:
    """Handles spaced repetition card retrieval and review submission.

    Attributes:
        _review_card_repository: Injected repository for review card operations.
    """

    def __init__(self, review_card_repository: AbstractReviewCardRepository) -> None:
        """Initialise the service with a review card repository.

        Args:
            review_card_repository: An AbstractReviewCardRepository implementation.
        """
        self._review_card_repository = review_card_repository

    async def get_due_cards(self, user_id: str, limit: int = 20) -> List[CardReviewResponse]:
        """Fetch cards due for review and resolve their flashcard content.

        Args:
            user_id: The reviewing user's document ID.
            limit: Maximum number of cards to return (default 20).

        Returns:
            List of CardReviewResponse objects with front/back content.
        """
        due_reviews: List[UserCardReview] = await self._review_card_repository.get_due_cards(
            user_id=user_id, limit=limit
        )
        responses: List[CardReviewResponse] = []
        for review in due_reviews:
            card: Optional[SpacedRepCard] = await self._review_card_repository.get_by_id(
                review.card_id
            )
            if card is None:
                continue
            responses.append(
                CardReviewResponse(
                    review_id=str(review.id),
                    card_id=str(card.id),
                    front=card.front,
                    back=card.back,
                    module_id=card.module_id,
                )
            )
        return responses

    async def submit_review(
        self, user_id: str, request: ReviewSubmitRequest
    ) -> ReviewSubmitResponse:
        """Process a card review submission using the SM-2 algorithm.

        Args:
            user_id: The reviewing user's document ID.
            request: Contains the review ID and quality rating.

        Returns:
            A ReviewSubmitResponse with the updated schedule.

        Raises:
            ResourceNotFoundError: If the review state cannot be found.
        """
        review: Optional[UserCardReview] = await self._review_card_repository.get_by_id(
            request.review_id
        )
        if review is None:
            raise ResourceNotFoundError("Review")

        updated = _apply_sm2(review=review, quality=request.quality)
        saved = await self._review_card_repository.save_review(updated)

        return ReviewSubmitResponse(
            review_id=str(saved.id),
            next_review_at=saved.next_review_at,
            interval_days=saved.interval_days,
        )
