"""Pydantic schemas for progress tracking endpoints."""

from typing import List

from pydantic import BaseModel


class CompleteTaskRequest(BaseModel):
    """Request body for marking a task as complete.

    Attributes:
        task_id (str): ID of the task to mark complete.
        module_id (str): ID of the parent module.
    """

    task_id: str
    module_id: str


class ModuleProgressResponse(BaseModel):
    """Progress summary for a single module.

    Attributes:
        module_id (str): ID of the module.
        tasks_completed (int): Count of completed tasks.
        tasks_total (int): Total tasks in the module.
        percent_complete (float): Completion percentage (0–100).
    """

    module_id: str
    tasks_completed: int
    tasks_total: int
    percent_complete: float


class ProgressOverviewResponse(BaseModel):
    """Full progress overview across all modules.

    Attributes:
        modules (List[ModuleProgressResponse]): Per-module progress entries.
        total_tasks_completed (int): Aggregate completed task count.
        total_xp (int): Total experience points earned.
    """

    modules: List[ModuleProgressResponse]
    total_tasks_completed: int
    total_xp: int
