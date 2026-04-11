"""Tests for spaced repetition review endpoints.

Stubs — full implementation pending review card seed fixtures.
"""

import pytest


@pytest.mark.asyncio
async def test_get_due_cards_returns_overdue_only() -> None:
    """GET /review/due returns only cards with next_review_at in the past. (stub)"""
    pass


@pytest.mark.asyncio
async def test_submit_review_updates_interval() -> None:
    """POST /review/submit updates next_review_at via SM-2. (stub)"""
    pass


@pytest.mark.asyncio
async def test_sm2_quality_zero_resets_interval() -> None:
    """Quality=0 review resets interval to 1 day and repetitions to 0. (stub)"""
    pass
