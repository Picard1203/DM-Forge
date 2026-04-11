"""Tests for curriculum endpoints: module listing, detail, and tasks.

Stubs — full implementation pending seeded test data fixtures.
"""

import pytest


@pytest.mark.asyncio
async def test_list_modules_returns_ordered_list() -> None:
    """GET /modules returns all modules in order. (stub)"""
    pass


@pytest.mark.asyncio
async def test_get_module_detail() -> None:
    """GET /modules/{id} returns module with embedded tasks. (stub)"""
    pass


@pytest.mark.asyncio
async def test_get_module_not_found() -> None:
    """GET /modules/{id} with unknown ID returns 404. (stub)"""
    pass


@pytest.mark.asyncio
async def test_list_module_tasks_ordered() -> None:
    """GET /modules/{id}/tasks returns tasks ordered by position. (stub)"""
    pass
