"""Curriculum seeder: loads YAML module/task files into MongoDB."""

import pathlib
from typing import Any, Dict, List

import yaml

from src.models.curriculum import Module, Task


_MODULES_DIR = pathlib.Path(__file__).parent.parent.parent / "curriculum" / "modules"


def _module_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalise module fields from a raw YAML dict.

    Args:
        data (Dict[str, Any]): Parsed YAML data for a module.

    Returns:
        (Dict[str, Any]): Field dict suitable for constructing a Module document.
    """
    return {
        "slug": data["slug"],
        "title": data["title"],
        "description": data.get("description", ""),
        "order": data.get("order", 0),
        "icon": data.get("icon"),
        "is_extension": data.get("is_extension", False),
        "estimated_hours": data.get("estimated_hours", 0),
        "xp_reward": data.get("xp_reward", 0),
    }


def _task_fields(task_data: Dict[str, Any], module_id: str) -> Dict[str, Any]:
    """Extract and normalise task fields from a raw YAML task entry.

    Args:
        task_data (Dict[str, Any]): Parsed YAML data for a single task.
        module_id (str): The string ID of the parent Module document.

    Returns:
        (Dict[str, Any]): Field dict suitable for constructing a Task document.
    """
    return {
        "module_id": module_id,
        "slug": task_data["slug"],
        "title": task_data["title"],
        "description": task_data.get("description", ""),
        "order": task_data.get("order", 0),
        "task_type": task_data.get("task_type", "reading"),
        "estimated_minutes": task_data.get("estimated_minutes", 0),
        "xp_reward": task_data.get("xp_reward", 0),
        "content": task_data.get("content", {}),
    }


async def _upsert_module(data: Dict[str, Any]) -> Module:
    """Insert or update a Module document by slug.

    Args:
        data (Dict[str, Any]): Parsed YAML data for the module.

    Returns:
        (Module): The persisted Module document (inserted or updated).
    """
    fields = _module_fields(data)
    existing = await Module.find_one(Module.slug == fields["slug"])
    if existing is None:
        module = Module(**fields)
        await module.insert()
        return module
    await existing.set(fields)
    return existing


async def _upsert_task(task_data: Dict[str, Any], module_id: str) -> None:
    """Insert or update a Task document by slug.

    Args:
        task_data (Dict[str, Any]): Parsed YAML data for the task.
        module_id (str): The string ID of the parent Module document.

    Returns:
        None
    """
    fields = _task_fields(task_data, module_id)
    existing = await Task.find_one(Task.slug == fields["slug"])
    if existing is None:
        task = Task(**fields)
        await task.insert()
        return
    await existing.set(fields)


async def seed_curriculum() -> None:
    """Upsert all modules and tasks from YAML files into MongoDB.

    Reads every .yaml file in the curriculum/modules directory, sorted by
    filename, and upserts each module and its tasks by slug. Safe to call on
    every startup — existing documents are updated, not duplicated.

    Returns:
        None
    """
    yaml_files: List[pathlib.Path] = sorted(_MODULES_DIR.glob("*.yaml"))
    for yaml_file in yaml_files:
        with yaml_file.open("r", encoding="utf-8") as fh:
            data: Dict[str, Any] = yaml.safe_load(fh)
        module = await _upsert_module(data)
        tasks: List[Dict[str, Any]] = data.get("tasks", [])
        for task_data in tasks:
            await _upsert_task(task_data, str(module.id))
