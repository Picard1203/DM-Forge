"""Beanie Document models for the Spaced Repetition review domain."""

from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class SpacedRepCard(Document):
    """MongoDB document defining a spaced-repetition flashcard.

    Attributes:
        module_id: Associated module ID for grouping.
        front: The prompt or question displayed to the user.
        back: The answer or explanation revealed on flip.
        tags: Free-form labels for filtering.
    """

    module_id: str
    front: str
    back: str
    tags: list = Field(default_factory=list)

    class Settings:
        name = "spaced_rep_cards"


class UserCardReview(Document):
    """MongoDB document recording a user's SM-2 state for a flashcard.

    Attributes:
        user_id: ID of the reviewing user.
        card_id: ID of the SpacedRepCard.
        easiness_factor: SM-2 easiness factor (default 2.5).
        interval_days: Current review interval in days.
        repetitions: Number of successful consecutive reviews.
        next_review_at: UTC timestamp of the next scheduled review.
        last_reviewed_at: UTC timestamp of the most recent review.
    """

    user_id: str
    card_id: str
    easiness_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0
    next_review_at: datetime = Field(default_factory=datetime.utcnow)
    last_reviewed_at: Optional[datetime] = None

    class Settings:
        name = "user_card_reviews"
