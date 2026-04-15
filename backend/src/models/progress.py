"""Beanie Document model for tracking individual task completion."""

from datetime import UTC, datetime
from typing import Optional

from beanie import Document
from pydantic import Field
from pymongo import ASCENDING, IndexModel


class UserProgress(Document):
    """MongoDB document recording a single task completion for a user.

    Attributes:
        user_id (str): ID of the user who completed the task.
        task_id (str): ID of the completed Task document.
        module_id (str): ID of the parent module for grouping queries.
        completed (bool): Whether the task has been marked complete.
        completed_at (Optional[datetime]): UTC timestamp of completion.
        xp_earned (int): XP awarded for this completion.
    """

    user_id: str
    task_id: str
    module_id: str
    completed: bool = False
    completed_at: Optional[datetime] = None
    xp_earned: int = 0

    class Settings:
        name = "user_progress"
        indexes = [
            IndexModel(
                [("user_id", ASCENDING), ("task_id", ASCENDING)],
                unique=True,
            )
        ]
