"""Tests for progress endpoints: task completion and overview."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_complete_task_awards_xp(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """POST /progress/complete awards XP on first task completion."""
    task = seeded_curriculum["task_one"]
    response = await client.post(
        "/api/v1/progress/complete",
        json={"task_id": str(task.id)},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["already_completed"] is False
    assert data["xp_earned"] == task.xp_reward
    assert data["new_xp"] == task.xp_reward
    assert data["new_level"] >= 1


@pytest.mark.asyncio
async def test_complete_task_duplicate_no_xp(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """POST /progress/complete on an already-done task awards 0 XP."""
    task = seeded_curriculum["task_one"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    await client.post(
        "/api/v1/progress/complete",
        json={"task_id": str(task.id)},
        headers=headers,
    )
    second = await client.post(
        "/api/v1/progress/complete",
        json={"task_id": str(task.id)},
        headers=headers,
    )
    assert second.status_code == 200
    data = second.json()
    assert data["already_completed"] is True
    assert data["xp_earned"] == 0


@pytest.mark.asyncio
async def test_complete_task_updates_module_percent(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """Completing one of two module tasks results in 50% progress."""
    task_one = seeded_curriculum["task_one"]
    module = seeded_curriculum["rules-fundamentals"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    await client.post(
        "/api/v1/progress/complete",
        json={"task_id": str(task_one.id)},
        headers=headers,
    )
    overview = await client.get(
        "/api/v1/progress/overview",
        headers=headers,
    )
    assert overview.status_code == 200
    modules = overview.json()["modules"]
    module_data = next(
        (mod for mod in modules if mod["module_id"] == str(module.id)), None
    )
    assert module_data is not None
    assert module_data["completed"] == 1
    assert module_data["total"] == 2
    assert module_data["percent"] == 50.0


@pytest.mark.asyncio
async def test_progress_overview_structure(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """GET /progress/overview returns the correct schema with all modules."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get("/api/v1/progress/overview", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "modules" in data
    assert "total_xp" in data
    assert isinstance(data["modules"], list)
    assert len(data["modules"]) == 2
    for mod in data["modules"]:
        assert "module_id" in mod
        assert "completed" in mod
        assert "total" in mod
        assert "percent" in mod
