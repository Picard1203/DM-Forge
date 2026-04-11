"""Tests for quiz endpoints: retrieval and answer submission.

Stubs — full implementation pending quiz seed fixtures.
"""

import pytest


@pytest.mark.asyncio
async def test_get_quiz_hides_correct_answers() -> None:
    """GET /quizzes/{id} does not expose correct_index. (stub)"""
    pass


@pytest.mark.asyncio
async def test_submit_quiz_correct_answers_passes() -> None:
    """Submitting all correct answers results in passed=True. (stub)"""
    pass


@pytest.mark.asyncio
async def test_submit_quiz_wrong_answers_fails() -> None:
    """Submitting wrong answers below threshold results in passed=False. (stub)"""
    pass


@pytest.mark.asyncio
async def test_submit_quiz_xp_awarded_only_on_first_pass() -> None:
    """XP is awarded only on the first passing attempt. (stub)"""
    pass
