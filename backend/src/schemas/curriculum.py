"""Pydantic schemas for curriculum endpoints."""

from typing import List, Optional

from pydantic import BaseModel


class TaskResponse(BaseModel):
    """Serialised Task returned from curriculum endpoints.

    Attributes:
        id (str): MongoDB document ID.
        module_id (str): Parent module ID.
        slug (str): URL-safe identifier.
        title (str): Display title.
        task_type (str): Category of task.
        content_url (Optional[str]): Optional external content URL.
        description (str): Short task description.
        order (int): Position within the module.
        estimated_minutes (int): Approximate completion time.
        xp_reward (int): XP awarded on completion.
        tags (List[str]): List of category tags.
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
        id (str): MongoDB document ID.
        slug (str): URL-safe identifier.
        title (str): Display title.
        description (str): Module overview text.
        order (int): Position in the curriculum.
        estimated_minutes (int): Total estimated completion time.
        icon (Optional[str]): Optional display icon.
        is_extension (bool): True if this is an extension module.
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
        tasks (List[TaskResponse]): Ordered list of tasks.
    """

    tasks: List[TaskResponse]
