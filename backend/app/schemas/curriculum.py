"""Pydantic schemas for curriculum endpoints."""

from typing import List, Optional

from pydantic import BaseModel


class TaskResponse(BaseModel):
    """Serialised Task returned from curriculum endpoints.

    Attributes:
        id: MongoDB document ID as a string.
        module_id: Parent module ID.
        slug: URL-safe identifier.
        title: Display title.
        task_type: Category of task.
        content_url: Optional external content URL.
        description: Short task description.
        order: Position within the module.
        estimated_minutes: Approximate completion time.
        xp_reward: XP awarded on completion.
        tags: List of category tags.
    """

    id: str
    module_id: str
    slug: str
    title: str
    task_type: str
    content_url: Optional[str]
    description: str
    order: int
    estimated_minutes: int
    xp_reward: int
    tags: List[str]


class ModuleResponse(BaseModel):
    """Serialised Module returned from curriculum endpoints.

    Attributes:
        id: MongoDB document ID as a string.
        slug: URL-safe identifier.
        title: Display title.
        description: Module overview text.
        order: Position in the curriculum.
        estimated_minutes: Total estimated completion time.
        icon: Optional display icon.
        is_extension: True if this is an extension module.
    """

    id: str
    slug: str
    title: str
    description: str
    order: int
    estimated_minutes: int
    icon: Optional[str]
    is_extension: bool


class ModuleDetailResponse(ModuleResponse):
    """Extended module response including the task list.

    Attributes:
        tasks: Ordered list of tasks within this module.
    """

    tasks: List[TaskResponse]
