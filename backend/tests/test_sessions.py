"""Tests for session plan builder.

Stubs — full implementation pending task/module test fixtures.
"""

import pytest


@pytest.mark.asyncio
async def test_session_plan_fits_time_budget() -> None:
    """Session plan total_minutes does not exceed available_minutes. (stub)"""
    pass


@pytest.mark.asyncio
async def test_session_plan_skips_completed_tasks() -> None:
    """Session plan excludes already-completed tasks. (stub)"""
    pass


@pytest.mark.asyncio
async def test_session_plan_empty_when_all_done() -> None:
    """Session plan returns empty items when all tasks are complete. (stub)"""
    pass
