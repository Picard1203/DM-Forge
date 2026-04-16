"""Pydantic schemas for spaced repetition review endpoints."""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ReviewCardResponse(BaseModel):
    """Serialised flashcard presented to the user for review.

    Attributes:
        id (str): MongoDB document ID of the ReviewCard.
        front (str): The question/prompt side of the card.
        back (str): The answer/explanation side of the card.
        tags (List[str]): Free-form labels.
    """

    id: str
    front: str
    back: str
    tags: List[str]


class ReviewSubmitRequest(BaseModel):
    """Request body for submitting the quality rating for a reviewed card.

    Attributes:
        card_id (str): MongoDB document ID of the ReviewCard that was reviewed.
        quality (int): SM-2 quality rating from 0 (complete blackout) to 5 (perfect).
    """

    card_id: str
    quality: int = Field(..., ge=0, le=5)


class ReviewSubmitResponse(BaseModel):
    """Response returned after processing a card review submission.

    Attributes:
        next_review (datetime): UTC timestamp of the next scheduled review.
        interval_days (int): New review interval in days.
        ease_factor (float): Updated SM-2 easiness factor.
    """

    next_review: datetime
    interval_days: int
    ease_factor: float
