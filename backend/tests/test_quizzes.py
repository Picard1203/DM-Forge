"""Tests for quiz endpoints: retrieval and answer submission."""

import pytest
from httpx import AsyncClient

from src.models.curriculum import Module
from src.models.quiz import Quiz, QuizQuestion


async def _seed_quiz(module: Module, passing_score: float = 0.7) -> Quiz:
    """Insert a Quiz with three multiple-choice questions and return it.

    Args:
        module (Module): The module to associate with the quiz.
        passing_score (float): Minimum fraction to pass.

    Returns:
        Quiz: The inserted Quiz document.
    """
    quiz = Quiz(
        slug="test-quiz",
        module_id=str(module.id),
        title="Test Quiz",
        description="A quiz for tests",
        passing_score=passing_score,
        xp_reward=50,
        questions=[
            QuizQuestion(
                question_text="What is 2+2?",
                question_type="multiple_choice",
                options=["3", "4", "5", "6"],
                correct_answer_index=1,
                explanation="2+2 equals 4.",
            ),
            QuizQuestion(
                question_text="What is the capital of France?",
                question_type="multiple_choice",
                options=["Berlin", "Madrid", "Paris", "Rome"],
                correct_answer_index=2,
                explanation="Paris is the capital of France.",
            ),
            QuizQuestion(
                question_text="Which number is prime?",
                question_type="multiple_choice",
                options=["4", "6", "7", "9"],
                correct_answer_index=2,
                explanation="7 is a prime number.",
            ),
        ],
    )
    await quiz.insert()
    return quiz


@pytest.mark.asyncio
async def test_get_quiz_hides_correct_answers(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """GET /quizzes/{id} does not expose correct_answer_index or explanation."""
    module = seeded_curriculum["rules-fundamentals"]
    quiz = await _seed_quiz(module)
    response = await client.get(
        f"/api/v1/quizzes/{quiz.id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(quiz.id)
    assert data["slug"] == "test-quiz"
    assert len(data["questions"]) == 3
    for question in data["questions"]:
        assert "correct_answer_index" not in question
        assert "explanation" not in question
        assert "question_text" in question
        assert "options" in question


@pytest.mark.asyncio
async def test_submit_quiz_correct_answers_passes(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """Submitting all correct answers results in passed=True and xp_earned > 0."""
    module = seeded_curriculum["rules-fundamentals"]
    quiz = await _seed_quiz(module)
    response = await client.post(
        f"/api/v1/quizzes/{quiz.id}/submit",
        json={"answers": [1, 2, 2]},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["passed"] is True
    assert data["score"] == 1.0
    assert data["xp_earned"] == 50
    assert data["already_completed"] is False
    assert len(data["question_results"]) == 3
    for result in data["question_results"]:
        assert result["correct"] is True


@pytest.mark.asyncio
async def test_submit_quiz_wrong_answers_fails(
    client: AsyncClient,
    auth_token: str,
    seeded_curriculum: dict,
) -> None:
    """Submitting all wrong answers results in passed=False and xp_earned=0."""
    module = seeded_curriculum["rules-fundamentals"]
    quiz = await _seed_quiz(module)
    response = await client.post(
        f"/api/v1/quizzes/{quiz.id}/submit",
        json={"answers": [0, 0, 0]},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["passed"] is False
    assert data["xp_earned"] == 0
    for result in data["question_results"]:
        assert result["correct"] is False
        assert "correct_answer_index" in result
        assert "explanation" in result


@pytest.mark.asyncio
async def test_submit_quiz_xp_awarded_only_on_first_pass(
    client: AsyncClient,
    auth_token: str,
    mock_user,
    seeded_curriculum: dict,
) -> None:
    """XP is awarded only on the first passing attempt; subsequent passes earn 0 XP."""
    module = seeded_curriculum["rules-fundamentals"]
    quiz = await _seed_quiz(module)
    correct_answers = {"answers": [1, 2, 2]}
    headers = {"Authorization": f"Bearer {auth_token}"}
    first_response = await client.post(
        f"/api/v1/quizzes/{quiz.id}/submit",
        json=correct_answers,
        headers=headers,
    )
    assert first_response.status_code == 200
    assert first_response.json()["xp_earned"] == 50
    assert first_response.json()["already_completed"] is False
    second_response = await client.post(
        f"/api/v1/quizzes/{quiz.id}/submit",
        json=correct_answers,
        headers=headers,
    )
    assert second_response.status_code == 200
    assert second_response.json()["xp_earned"] == 0
    assert second_response.json()["already_completed"] is True
