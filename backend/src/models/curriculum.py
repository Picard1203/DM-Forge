"""Beanie Document models for the Curriculum domain (Modules and Tasks)."""

from beanie import Document


class Module(Document):
    """MongoDB document representing a high-level learning module.

    Attributes:
        title (str): Grouping title for a set of related tasks.
        description (str): Short summary of the module's target outcomes.
        order (int): Sort position for display in the curriculum.
    """

    title: str
    description: str = ""
    order: int = 0

    class Settings:
        name = "modules"


class Task(Document):
    """MongoDB document representing a specific learning activity.

    Attributes:
        module_id (str): Reference to the parent Module.
        title (str): Short name for the task.
        description (str): Detailed instructions or content summary.
        xp_reward (int): XP awarded upon completion.
        estimated_minutes (int): Expected time commitment.
        order (int): Sort position within the parent module.
    """

    module_id: str
    title: str
    description: str = ""
    xp_reward: int = 10
    estimated_minutes: int = 5
    order: int = 0

    class Settings:
        name = "tasks"
