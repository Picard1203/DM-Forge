"""Beanie Document models for Spaced Repetition (Review Cards)."""

from datetime import UTC, datetime
from typing import List, Optional

from beanie import Document
from pydantic import Field


class ReviewCard(Document):
    """MongoDB document representing a static review card in a module.

    Attributes:
        module_id (str): Associated module ID for grouping.
        front (str): The prompt or question displayed to the user.
        back (str): The answer or explanation revealed on flip.
        tags (List[str]): Free-form labels for filtering.
    """

    module_id: str
    front: str
    back: str
    tags: List[str] = Field(default_factory=list)

    class Settings:
        name = "review_cards"


class UserCardReview(Document):
    """MongoDB record tracking a user's mastery of a review card using SM-2.

    Attributes:
        user_id (str): ID of the reviewing user.
        card_id (str): ID of the ReviewCard.
        ease_factor (float): SM-2 easiness factor (default 2.5).
        interval_days (int): Current review interval in days.
        repetitions (int): Number of successful consecutive reviews.
        next_review (datetime): UTC timestamp of the next scheduled review.
        last_reviewed (Optional[datetime]): UTC timestamp of the most recent review.
    """

    user_id: str
    card_id: str
    ease_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0
    next_review: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_reviewed: Optional[datetime] = None

    class Settings:
        name = "user_card_reviews"
