"""Curriculum seeder: loads YAML module/task files into MongoDB.

Usage:
    python -m src.seeders.seed_curriculum

The seeder reads all YAML files under backend/curriculum/modules/ and upserts
them into MongoDB so that running it multiple times is idempotent.
"""

import asyncio
import pathlib
from typing import Any, Dict, List

import yaml

from src.database import init_db
from src.models.curriculum import Module, Task


_MODULES_DIR = pathlib.Path(__file__).parent.parent.parent / "curriculum" / "modules"


async def seed_modules() -> None:
    """Load all module YAML files and upsert into MongoDB.

    For each module file:
    - Upserts the Module document by slug.
    - Upserts each Task document by slug.
    """
    await init_db()
    yaml_files: List[pathlib.Path] = sorted(_MODULES_DIR.glob("*.yaml"))

    for yaml_file in yaml_files:
        with yaml_file.open("r", encoding="utf-8") as fh:
            data: Dict[str, Any] = yaml.safe_load(fh)

        existing_module = await Module.find_one(Module.slug == data["slug"])
        if existing_module is None:
            module = Module(
                slug=data["slug"],
                title=data["title"],
                description=data.get("description", ""),
                order=data.get("order", 0),
                estimated_minutes=data.get("estimated_minutes", 30),
                icon=data.get("icon"),
                is_extension=data.get("is_extension", False),
            )
            await module.insert()
        else:
            module = existing_module

        tasks: List[Dict[str, Any]] = data.get("tasks", [])
        for task_data in tasks:
            existing_task = await Task.find_one(Task.slug == task_data["slug"])
            if existing_task is None:
                task = Task(
                    module_id=str(module.id),
                    slug=task_data["slug"],
                    title=task_data["title"],
                    task_type=task_data.get("task_type", "reading"),
                    content_url=task_data.get("content_url"),
                    description=task_data.get("description", ""),
                    order=task_data.get("order", 0),
                    estimated_minutes=task_data.get("estimated_minutes", 5),
                    xp_reward=task_data.get("xp_reward", 10),
                    tags=task_data.get("tags", []),
                )
                await task.insert()

        print(f"Seeded module: {data['slug']} ({len(tasks)} tasks)")


if __name__ == "__main__":
    asyncio.run(seed_modules())
