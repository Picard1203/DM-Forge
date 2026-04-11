"""Beanie Document models for the Curriculum domain."""

from typing import List, Optional

from beanie import Document
from pydantic import Field


class Task(Document):
    """MongoDB document representing a single learning task within a module.

    Attributes:
        module_id: Reference to the parent Module document id.
        slug: URL-safe unique identifier for this task.
        title: Human-readable task title.
        task_type: Category of task (e.g. "video", "reading", "quiz").
        content_url: Optional URL pointing to external content.
        description: Short summary of the task.
        order: Zero-based position within the parent module.
        estimated_minutes: Approximate time to complete.
        xp_reward: Experience points awarded on completion.
        tags: Free-form labels for filtering and search.
    """

    module_id: str
    slug: str
    title: str
    task_type: str
    content_url: Optional[str] = None
    description: str = ""
    order: int = 0
    estimated_minutes: int = 5
    xp_reward: int = 10
    tags: List[str] = Field(default_factory=list)

    class Settings:
        name = "tasks"


class Module(Document):
    """MongoDB document representing a learning module (collection of tasks).

    Attributes:
        slug: URL-safe unique identifier for this module.
        title: Human-readable module title.
        description: Multi-sentence overview of the module content.
        order: Zero-based position in the overall curriculum ordering.
        estimated_minutes: Total estimated time to complete all tasks.
        icon: Optional emoji or icon identifier for display.
        is_extension: True if this is an extension module rather than core.
    """

    slug: str
    title: str
    description: str = ""
    order: int = 0
    estimated_minutes: int = 30
    icon: Optional[str] = None
    is_extension: bool = False

    class Settings:
        name = "modules"
