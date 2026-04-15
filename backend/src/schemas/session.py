"""Pydantic schemas for the time-aware session builder endpoints."""

from typing import List

from pydantic import BaseModel, Field


class SessionRequest(BaseModel):
    """Request body for generating a session plan.

    Attributes:
        available_minutes (int): Time the user has available for this session.
    """

    available_minutes: int = Field(..., ge=5, le=480)


class SessionTaskItem(BaseModel):
    """A single task scheduled within a session plan.

    Attributes:
        task_id (str): MongoDB ID of the task.
        slug (str): URL-safe task identifier.
        title (str): Display name for the task.
        task_type (str): Category of activity.
        estimated_minutes (int): Time allocated to this task in minutes.
        xp_reward (int): XP earned upon completion.
    """

    task_id: str
    slug: str
    title: str
    task_type: str
    estimated_minutes: int
    xp_reward: int


class SessionPlanResponse(BaseModel):
    """A fully constructed time-aware session plan.

    Attributes:
        tasks (List[SessionTaskItem]): Ordered list of tasks fitting the budget.
        total_minutes (int): Sum of time across all selected tasks.
        has_review_slot (bool): True when time was reserved for a review session.
    """

    tasks: List[SessionTaskItem]
    total_minutes: int
    has_review_slot: bool
