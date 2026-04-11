"""Pydantic schemas for spaced repetition review endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field


class CardReviewResponse(BaseModel):
    """Serialised flashcard presented to the user for review.

    Attributes:
        review_id: ID of the UserCardReview document (tracks SM-2 state).
        card_id: ID of the SpacedRepCard.
        front: The question/prompt side of the card.
        back: The answer/explanation side of the card.
        module_id: Associated module ID.
    """

    review_id: str
    card_id: str
    front: str
    back: str
    module_id: str


class ReviewSubmitRequest(BaseModel):
    """Request body for submitting the quality rating after reviewing a card.

    Attributes:
        review_id: ID of the UserCardReview to update.
        quality: SM-2 quality rating from 0 (complete blackout) to 5 (perfect).
    """

    review_id: str
    quality: int = Field(..., ge=0, le=5)


class ReviewSubmitResponse(BaseModel):
    """Response returned after processing a card review submission.

    Attributes:
        review_id: ID of the updated UserCardReview.
        next_review_at: UTC timestamp of the next scheduled review.
        interval_days: New review interval in days.
    """

    review_id: str
    next_review_at: datetime
    interval_days: int
