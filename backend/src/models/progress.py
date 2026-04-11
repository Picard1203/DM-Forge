"""Beanie Document models for tracking user learning progress."""

from datetime import UTC, datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class TaskCompletion(Document):
    """MongoDB document recording a single task completion event.

    Attributes:
        user_id (str): ID of the user who completed the task.
        task_id (str): ID of the completed Task document.
        module_id (str): ID of the parent module for denormalised queries.
        xp_awarded (int): XP given at time of completion.
        completed_at (datetime): UTC timestamp of completion.
    """

    user_id: str
    task_id: str
    module_id: str
    xp_awarded: int = 0
    completed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "task_completions"


class UserProgress(Document):
    """MongoDB document summarising a user's progress on a module.

    Attributes:
        user_id (str): ID of the user.
        module_id (str): ID of the Module document.
        tasks_completed (int): Count of completed tasks in this module.
        tasks_total (int): Total tasks in this module at time of last sync.
        percent_complete (float): Derived percentage for display.
        started_at (datetime): UTC timestamp when the user first engaged.
        completed_at (Optional[datetime]): UTC timestamp when all tasks were finished.
    """

    user_id: str
    module_id: str
    tasks_completed: int = 0
    tasks_total: int = 0
    percent_complete: float = 0.0
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: Optional[datetime] = None

    class Settings:
        name = "user_progress"
