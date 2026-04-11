"""Pydantic schemas for the time-aware session builder endpoints."""

from typing import List

from pydantic import BaseModel, Field

from src.schemas.curriculum import TaskResponse


class SessionRequest(BaseModel):
    """Request body for generating a session plan.

    Attributes:
        available_minutes: Time the user has available for this session.
    """

    available_minutes: int = Field(..., ge=5, le=240)


class SessionTaskItem(BaseModel):
    """A single task scheduled within a session plan.

    Attributes:
        task: The task to complete.
        estimated_minutes: Time allocated to this task in the session.
    """

    task: TaskResponse
    estimated_minutes: int


class SessionPlanResponse(BaseModel):
    """A fully constructed session plan.

    Attributes:
        items: Ordered list of task items fitting within the time budget.
        total_minutes: Sum of all task time allocations.
        xp_potential: Total XP available if all tasks are completed.
    """

    items: List[SessionTaskItem]
    total_minutes: int
    xp_potential: int
