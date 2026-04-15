"""Pydantic schemas for progress tracking endpoints."""

from typing import List

from pydantic import BaseModel

from src.schemas.achievement import AchievementResponse


class CompleteTaskRequest(BaseModel):
    """Request body for marking a task as complete.

    Attributes:
        task_id (str): ID of the task to mark complete.
    """

    task_id: str


class CompleteTaskResponse(BaseModel):
    """Response after a task completion attempt.

    Attributes:
        already_completed (bool): True if the task was already marked done.
        xp_earned (int): XP awarded in this request (0 if already completed).
        new_xp (int): User's total XP after this request.
        new_level (int): User's level after this request.
        earned_achievements (List[AchievementResponse]): Achievements unlocked.
    """

    already_completed: bool
    xp_earned: int
    new_xp: int
    new_level: int
    earned_achievements: List[AchievementResponse] = []


class ModuleProgressItem(BaseModel):
    """Progress summary for a single module.

    Attributes:
        module_id (str): ID of the module.
        completed (int): Count of tasks completed in the module.
        total (int): Total number of tasks in the module.
        percent (float): Completion percentage (0–100).
    """

    module_id: str
    completed: int
    total: int
    percent: float


class ProgressOverviewResponse(BaseModel):
    """Full progress overview across all modules for a user.

    Attributes:
        modules (List[ModuleProgressItem]): Per-module progress entries.
        total_xp (int): Sum of XP earned across all completed tasks.
    """

    modules: List[ModuleProgressItem]
    total_xp: int
