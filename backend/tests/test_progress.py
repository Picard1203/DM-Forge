"""Tests for progress endpoints: task completion and overview.

Stubs — full implementation pending task/module test fixtures.
"""

import pytest


@pytest.mark.asyncio
async def test_complete_task_awards_xp() -> None:
    """POST /progress/complete awards XP on first completion. (stub)"""
    pass


@pytest.mark.asyncio
async def test_complete_task_duplicate_no_xp() -> None:
    """POST /progress/complete on already-done task awards 0 XP. (stub)"""
    pass


@pytest.mark.asyncio
async def test_complete_task_updates_module_percent() -> None:
    """Completing tasks recalculates module progress percentage. (stub)"""
    pass


@pytest.mark.asyncio
async def test_progress_overview_structure() -> None:
    """GET /progress/overview returns correct schema. (stub)"""
    pass
