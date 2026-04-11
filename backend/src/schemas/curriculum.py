"""Pydantic schemas for curriculum endpoints."""

from typing import Any, Dict, Optional

from pydantic import BaseModel


class ModuleResponse(BaseModel):
    """Serialised Module returned from curriculum endpoints.

    Attributes:
        id (str): MongoDB document ID.
        slug (str): URL-safe identifier.
        title (str): Display title.
        description (str): Module overview text.
        order (int): Position in the curriculum.
        icon (Optional[str]): Optional display icon glyph.
        is_extension (bool): True if this is an optional extension module.
        estimated_hours (int): Approximate hours to complete the module.
        xp_reward (int): Total XP awarded upon module completion.
    """

    id: str
    slug: str
    title: str
    description: str
    order: int
    icon: Optional[str]
    is_extension: bool
    estimated_hours: int
    xp_reward: int


class TaskResponse(BaseModel):
    """Serialised Task returned from curriculum endpoints.

    Attributes:
        id (str): MongoDB document ID.
        slug (str): URL-safe identifier.
        title (str): Display title.
        description (str): Short task description.
        order (int): Position within the parent module.
        task_type (str): Category of activity (video, reading, exercise, etc.).
        estimated_minutes (int): Approximate completion time in minutes.
        xp_reward (int): XP awarded on completion.
        content (Dict[str, Any]): Type-specific payload from the YAML definition.
    """

    id: str
    slug: str
    title: str
    description: str
    order: int
    task_type: str
    estimated_minutes: int
    xp_reward: int
    content: Dict[str, Any]
