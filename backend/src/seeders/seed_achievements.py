"""Seeder: load achievements YAML and upsert Achievement documents."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from src.models.achievement import Achievement


async def seed_achievements() -> None:
    """Read curriculum/achievements.yaml and upsert each achievement by slug.

    Returns:
        None
    """
    yaml_path = Path(__file__).resolve().parents[3] / "curriculum" / "achievements.yaml"
    if not yaml_path.exists():
        return
    await _seed_file(yaml_path)


async def _seed_file(yaml_path: Path) -> None:
    """Load the achievements YAML and upsert each entry.

    Args:
        yaml_path (Path): Absolute path to achievements.yaml.

    Returns:
        None
    """
    with open(yaml_path, "r", encoding="utf-8") as file_handle:
        data: Dict[str, Any] = yaml.safe_load(file_handle)
    achievement_entries: List[Dict[str, Any]] = data.get("achievements", [])
    for entry in achievement_entries:
        await _upsert_achievement(entry)


async def _upsert_achievement(entry: Dict[str, Any]) -> None:
    """Insert or update a single Achievement document from a YAML entry.

    Args:
        entry (Dict[str, Any]): Parsed YAML dictionary for one achievement.

    Returns:
        None
    """
    slug: str = entry.get("slug", "")
    existing: Optional[Achievement] = await Achievement.find_one(Achievement.slug == slug)
    if existing is not None:
        existing.title = entry.get("title", existing.title)
        existing.description = entry.get("description", existing.description)
        existing.icon = entry.get("icon", existing.icon)
        existing.trigger_type = entry.get("trigger_type", existing.trigger_type)
        existing.trigger_value = str(entry.get("trigger_value", existing.trigger_value))
        existing.xp_reward = int(entry.get("xp_reward", existing.xp_reward))
        await existing.save()
    else:
        achievement = Achievement(
            slug=slug,
            title=entry.get("title", ""),
            description=entry.get("description", ""),
            icon=entry.get("icon", "award"),
            trigger_type=entry.get("trigger_type", ""),
            trigger_value=str(entry.get("trigger_value", "")),
            xp_reward=int(entry.get("xp_reward", 0)),
        )
        await achievement.insert()
