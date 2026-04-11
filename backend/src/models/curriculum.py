"""Beanie Document models for the Curriculum domain (Modules and Tasks)."""

from typing import Any, Dict, Optional

from beanie import Document
from pydantic import Field


class Module(Document):
    """MongoDB document representing a high-level learning module.

    Attributes:
        slug (str): URL-safe unique identifier for the module.
        title (str): Grouping title for a set of related tasks.
        description (str): Short summary of the module's target outcomes.
        order (int): Sort position for display in the curriculum.
        icon (Optional[str]): Glyph or emoji used as the module icon.
        is_extension (bool): Whether the module is optional extension content.
        estimated_hours (int): Approximate hours to complete the module.
        xp_reward (int): Total XP awarded upon module completion.
    """

    slug: str
    title: str
    description: str = ""
    order: int = 0
    icon: Optional[str] = None
    is_extension: bool = False
    estimated_hours: int = 0
    xp_reward: int = 0

    class Settings:
        name = "modules"


class Task(Document):
    """MongoDB document representing a specific learning activity.

    Attributes:
        module_id (str): Reference to the parent Module document id.
        slug (str): URL-safe unique identifier for the task.
        title (str): Short name for the task.
        description (str): Detailed instructions or content summary.
        order (int): Sort position within the parent module.
        task_type (str): Category of activity (video, reading, exercise, etc.).
        estimated_minutes (int): Expected time commitment in minutes.
        xp_reward (int): XP awarded upon task completion.
        content (Dict[str, Any]): Type-specific payload from the YAML definition.
    """

    module_id: str
    slug: str
    title: str
    description: str = ""
    order: int = 0
    task_type: str = ""
    estimated_minutes: int = 0
    xp_reward: int = 0
    content: Dict[str, Any] = Field(default_factory=dict)

    class Settings:
        name = "tasks"
