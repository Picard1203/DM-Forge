"""Beanie Document models for the Quiz domain."""

from datetime import UTC, datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field


class QuizQuestion(BaseModel):
    """Embedded model representing a single question within a Quiz document.

    Attributes:
        question_text (str): The question prompt shown to the user.
        question_type (str): Category — multiple_choice or scenario.
        options (List[str]): Answer option strings shown to the user.
        correct_answer_index (int): Zero-based index of the correct option.
        explanation (str): Explanation shown after the user answers.
        scenario_context (Optional[str]): Optional context paragraph for scenario questions.
    """

    question_text: str
    question_type: str = "multiple_choice"
    options: List[str] = Field(default_factory=list)
    correct_answer_index: int = 0
    explanation: str = ""
    scenario_context: Optional[str] = None


class Quiz(Document):
    """MongoDB document representing a quiz linked to a curriculum module.

    Attributes:
        slug (str): Unique URL-friendly identifier.
        module_id (str): Associated module document ID.
        title (str): Human-readable quiz title.
        description (str): Short description shown before starting.
        passing_score (float): Minimum fraction required to pass (0.0–1.0).
        xp_reward (int): XP awarded on first passing attempt.
        questions (List[QuizQuestion]): Embedded ordered list of questions.
    """

    slug: str
    module_id: str
    title: str
    description: str = ""
    passing_score: float = 0.7
    xp_reward: int = 50
    questions: List[QuizQuestion] = Field(default_factory=list)

    class Settings:
        name = "quizzes"


class QuizAttempt(Document):
    """MongoDB document recording a user's attempt at a quiz.

    Attributes:
        user_id (str): ID of the user.
        quiz_id (str): ID of the attempted Quiz.
        answers (List[int]): Selected answer index per question, in question order.
        score (float): Fraction of questions answered correctly (0.0–1.0).
        passed (bool): Whether the score met the passing threshold.
        completed_at (datetime): UTC timestamp of the attempt.
    """

    user_id: str
    quiz_id: str
    answers: List[int] = Field(default_factory=list)
    score: float = 0.0
    passed: bool = False
    completed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "quiz_attempts"
