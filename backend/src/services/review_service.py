"""Review service: spaced repetition scheduling using the SM-2 algorithm."""

from datetime import UTC, datetime, timedelta
from typing import List, Optional

from src.models.review_card import ReviewCard, UserCardReview
from src.repositories.abstract.review_card_repository import AbstractReviewCardRepository
from src.schemas.review import ReviewCardResponse, ReviewSubmitRequest, ReviewSubmitResponse
from src.utils.exceptions import ResourceNotFoundError

_MIN_EASE_FACTOR: float = 1.3


def _apply_sm2(review: UserCardReview, quality: int) -> UserCardReview:
    """Apply the SM-2 algorithm to update a card's scheduling state.

    Args:
        review (UserCardReview): The current UserCardReview state.
        quality (int): Response quality from 0 (blackout) to 5 (perfect).

    Returns:
        UserCardReview: The updated review with new interval, ease factor, and next review date.
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
            review.interval_days = round(review.interval_days * review.ease_factor)
        review.repetitions += 1
    new_ef = review.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    review.ease_factor = max(_MIN_EASE_FACTOR, new_ef)
    review.next_review = datetime.now(UTC) + timedelta(days=review.interval_days)
    review.last_reviewed = datetime.now(UTC)
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

    async def get_due_cards(self, user_id: str) -> List[ReviewCardResponse]:
        """Fetch cards due for review and return them as serialised responses.

        Args:
            user_id (str): The reviewing user's document ID.

        Returns:
            List[ReviewCardResponse]: Cards due for review (overdue or never reviewed).
        """
        due_cards: List[ReviewCard] = await self._review_card_repository.get_due_cards(
            user_id=user_id
        )
        responses: List[ReviewCardResponse] = []
        for card in due_cards:
            responses.append(
                ReviewCardResponse(
                    id=str(card.id),
                    front=card.front,
                    back=card.back,
                    tags=card.tags,
                )
            )
        return responses

    async def submit_review(
        self, user_id: str, request: ReviewSubmitRequest
    ) -> ReviewSubmitResponse:
        """Process a card review submission using the SM-2 algorithm.

        Looks up or creates the UserCardReview record, applies SM-2 scheduling,
        saves the updated state, and returns the new schedule.

        Args:
            user_id (str): The reviewing user's document ID.
            request (ReviewSubmitRequest): Contains card_id and quality rating.

        Returns:
            ReviewSubmitResponse: Updated schedule with next_review date and interval.

        Raises:
            ResourceNotFoundError: If no ReviewCard with the given card_id exists.
        """
        card: Optional[ReviewCard] = await self._review_card_repository.get_card_by_id(
            request.card_id
        )
        if card is None:
            raise ResourceNotFoundError("ReviewCard")
        review: Optional[UserCardReview] = await self._review_card_repository.get_review_record(
            user_id=user_id, card_id=request.card_id
        )
        if review is None:
            review = UserCardReview(user_id=user_id, card_id=request.card_id)
        updated = _apply_sm2(review=review, quality=request.quality)
        saved = await self._review_card_repository.save_review(updated)
        return ReviewSubmitResponse(
            next_review=saved.next_review,
            interval_days=saved.interval_days,
            ease_factor=saved.ease_factor,
        )
