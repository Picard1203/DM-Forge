"""Tests for curriculum endpoints: module listing, detail, and tasks."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_modules_returns_ordered_list(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """GET /modules returns all modules sorted by order ascending."""
    response = await client.get(
        "/api/v1/modules",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert payload[0]["order"] <= payload[1]["order"]


@pytest.mark.asyncio
async def test_get_module_detail(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """GET /modules/{slug} returns the matching module by slug."""
    response = await client.get(
        "/api/v1/modules/rules-fundamentals",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["slug"] == "rules-fundamentals"
    assert payload["title"] == "Rules Fundamentals"


@pytest.mark.asyncio
async def test_get_module_not_found(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """GET /modules/{slug} with an unknown slug returns 404."""
    response = await client.get(
        "/api/v1/modules/nonexistent-module",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_module_tasks_ordered(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """GET /modules/{slug}/tasks returns tasks sorted by order ascending."""
    response = await client.get(
        "/api/v1/modules/rules-fundamentals/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2
    orders = []
    for task in tasks:
        orders.append(task["order"])
    assert orders == sorted(orders)
