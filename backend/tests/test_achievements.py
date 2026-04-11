"""Tests for achievement trigger checking and awarding.

Stubs — full implementation pending achievement seed fixtures.
"""

import pytest


@pytest.mark.asyncio
async def test_achievement_awarded_on_trigger_threshold() -> None:
    """Achievement is awarded when current_value meets trigger_value. (stub)"""
    pass


@pytest.mark.asyncio
async def test_achievement_not_awarded_twice() -> None:
    """Achievement is not awarded again if already earned. (stub)"""
    pass


@pytest.mark.asyncio
async def test_list_achievements_returns_all() -> None:
    """GET /achievements returns all achievement definitions. (stub)"""
    pass
