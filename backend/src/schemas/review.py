"""Pydantic schemas for spaced repetition review endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field


class CardReviewResponse(BaseModel):
    """Serialised flashcard presented to the user for review.

    Attributes:
        review_id (str): ID of the UserCardReview document (SM-2 state).
        card_id (str): ID of the SpacedRepCard.
        front (str): The question/prompt side of the card.
        back (str): The answer/explanation side of the card.
        module_id (str): Associated module ID.
    """

    review_id: str
    card_id: str
    front: str
    back: str
    module_id: str


class ReviewSubmitRequest(BaseModel):
    """Request body for submitting the quality rating for a card.

    Attributes:
        review_id (str): ID of the UserCardReview to update.
        quality (int): SM-2 quality rating from 0 to 5.
    """

    review_id: str
    quality: int = Field(..., ge=0, le=5)


class ReviewSubmitResponse(BaseModel):
    """Response returned after processing a card review submission.

    Attributes:
        review_id (str): ID of the updated UserCardReview.
        next_review_at (datetime): UTC timestamp of the next review.
        interval_days (int): New review interval in days.
    """

    review_id: str
    next_review_at: datetime
    interval_days: int
