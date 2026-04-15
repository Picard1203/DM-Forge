"""Tests for the time-aware session plan builder endpoint."""

import pytest
from httpx import AsyncClient

from src.models.curriculum import Module, Task
from src.models.progress import UserProgress
from datetime import UTC, datetime


async def _seed_module_with_tasks(
    slug: str, order: int, task_minutes: list
) -> tuple:
    """Insert a module and tasks with given estimated_minutes values.

    Args:
        slug (str): Module slug.
        order (int): Module display order.
        task_minutes (list): Estimated minutes for each task to create.

    Returns:
        tuple: (module, list_of_tasks)
    """
    module = Module(
        slug=slug,
        title=slug.replace("-", " ").title(),
        description="Test module",
        order=order,
        estimated_hours=1,
        xp_reward=100,
        is_extension=False,
    )
    await module.insert()
    tasks = []
    for idx, minutes in enumerate(task_minutes):
        task = Task(
            module_id=str(module.id),
            slug=f"{slug}-task-{idx}",
            title=f"Task {idx}",
            description="Test task",
            order=idx + 1,
            task_type="reading",
            estimated_minutes=minutes,
            xp_reward=10,
            content={},
        )
        await task.insert()
        tasks.append(task)
    return module, tasks


@pytest.mark.asyncio
async def test_session_plan_fits_time_budget(
    client: AsyncClient,
    auth_token: str,
) -> None:
    """Session plan total_minutes does not exceed available_minutes."""
    await _seed_module_with_tasks("mod-a", 1, [10, 15, 20, 30])
    response = await client.post(
        "/api/v1/sessions/plan",
        json={"available_minutes": 30},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_minutes"] <= 30
    assert isinstance(data["tasks"], list)


@pytest.mark.asyncio
async def test_session_plan_skips_completed_tasks(
    client: AsyncClient,
    auth_token: str,
    mock_user,
) -> None:
    """Session plan excludes tasks the user has already completed."""
    _module, tasks = await _seed_module_with_tasks("mod-b", 1, [10, 10])
    task_to_complete = tasks[0]
    progress = UserProgress(
        user_id=str(mock_user.id),
        task_id=str(task_to_complete.id),
        module_id=str(_module.id),
        completed=True,
        completed_at=datetime.now(UTC),
        xp_earned=10,
    )
    await progress.insert()
    response = await client.post(
        "/api/v1/sessions/plan",
        json={"available_minutes": 60},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    task_ids = [item["task_id"] for item in response.json()["tasks"]]
    assert str(task_to_complete.id) not in task_ids
    assert str(tasks[1].id) in task_ids


@pytest.mark.asyncio
async def test_session_plan_empty_when_all_done(
    client: AsyncClient,
    auth_token: str,
    mock_user,
) -> None:
    """Session plan returns an empty task list when all tasks are complete."""
    _module, tasks = await _seed_module_with_tasks("mod-c", 1, [5, 10])
    for task in tasks:
        progress = UserProgress(
            user_id=str(mock_user.id),
            task_id=str(task.id),
            module_id=str(_module.id),
            completed=True,
            completed_at=datetime.now(UTC),
            xp_earned=10,
        )
        await progress.insert()
    response = await client.post(
        "/api/v1/sessions/plan",
        json={"available_minutes": 60},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.json()["tasks"] == []


@pytest.mark.asyncio
async def test_session_plan_includes_review_slot_when_enough_time(
    client: AsyncClient,
    auth_token: str,
) -> None:
    """has_review_slot is True when available_minutes is at least 15."""
    await _seed_module_with_tasks("mod-d", 1, [5])
    response = await client.post(
        "/api/v1/sessions/plan",
        json={"available_minutes": 15},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.json()["has_review_slot"] is True

    response_short = await client.post(
        "/api/v1/sessions/plan",
        json={"available_minutes": 10},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response_short.status_code == 200
    assert response_short.json()["has_review_slot"] is False
