"""Review service: spaced repetition scheduling using the SM-2 algorithm."""

from datetime import UTC, datetime, timedelta
from typing import List, Optional

from src.models.review_card import SpacedRepCard, UserCardReview
from src.repositories.abstract.review_card_repository import AbstractReviewCardRepository
from src.schemas.review import CardReviewResponse, ReviewSubmitRequest, ReviewSubmitResponse
from src.utils.exceptions import ResourceNotFoundError


def _apply_sm2(review: UserCardReview, quality: int) -> UserCardReview:
    """Apply the SM-2 algorithm to update a card's scheduling state.

    Args:
        review (UserCardReview): The current UserCardReview state.
        quality (int): Response quality from 0 to 5.

    Returns:
        UserCardReview: The updated review with new interval and EF.
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
    review.next_review_at = datetime.now(UTC) + timedelta(days=review.interval_days)
    review.last_reviewed_at = datetime.now(UTC)
    return review


class ReviewService:
    """Handles spaced repetition card retrieval and review submission.

    Attributes:
        _review_card_repository (AbstractReviewCardRepository): Injected repository.
    """

    def __init__(self, review_card_repository: AbstractReviewCardRepository) -> None:
        """Initialise the service with a review card repository.

        Args:
            review_card_repository (AbstractReviewCardRepository): Repository instance.
        """
        self._review_card_repository = review_card_repository

    async def get_due_cards(self, user_id: str, limit: int = 20) -> List[CardReviewResponse]:
        """Fetch cards due for review and resolve their flashcard content.

        Args:
            user_id (str): The reviewing user's document ID.
            limit (int): Maximum number of cards to return.

        Returns:
            List[CardReviewResponse]: List of CardReviewResponse objects.
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
            user_id (str): The reviewing user's document ID.
            request (ReviewSubmitRequest): The review ID and quality.

        Returns:
            ReviewSubmitResponse: Response with the updated schedule.

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
