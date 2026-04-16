"""Seeder: load review card YAML files and upsert ReviewCard documents."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from src.models.curriculum import Module
from src.models.review_card import ReviewCard


async def seed_review_cards() -> None:
    """Read every YAML under curriculum/review_cards/ and upsert by (module_id, front).

    Returns:
        None
    """
    card_dir = Path(__file__).resolve().parents[2] / "curriculum" / "review_cards"
    if not card_dir.exists():
        return
    yaml_files = sorted(card_dir.glob("*.yaml"))
    for yaml_path in yaml_files:
        await _seed_file(yaml_path)


async def _seed_file(yaml_path: Path) -> None:
    """Load one YAML file and upsert each review card entry.

    Args:
        yaml_path (Path): Absolute path to the YAML file.

    Returns:
        None
    """
    with open(yaml_path, "r", encoding="utf-8") as file_handle:
        data: Dict[str, Any] = yaml.safe_load(file_handle)
    card_entries: List[Dict[str, Any]] = data.get("review_cards", [])
    for entry in card_entries:
        await _upsert_card(entry)


async def _upsert_card(entry: Dict[str, Any]) -> None:
    """Insert or update a single ReviewCard document from a YAML entry.

    Args:
        entry (Dict[str, Any]): Parsed YAML dictionary for one card.

    Returns:
        None
    """
    module_slug: str = entry.get("module_slug", "")
    module: Optional[Module] = await Module.find_one(Module.slug == module_slug)
    if module is None:
        return
    module_id = str(module.id)
    front: str = entry.get("front", "")
    existing: Optional[ReviewCard] = await ReviewCard.find_one(
        ReviewCard.module_id == module_id,
        ReviewCard.front == front,
    )
    tags: List[str] = entry.get("tags", [])
    back: str = entry.get("back", "")
    if existing is not None:
        existing.back = back
        existing.tags = tags
        await existing.save()
    else:
        card = ReviewCard(
            module_id=module_id,
            front=front,
            back=back,
            tags=tags,
        )
        await card.insert()
