"""Beanie Document models for the Quiz domain."""

from datetime import UTC, datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field


class QuizQuestion(Document):
    """MongoDB document representing a single quiz question.

    Attributes:
        quiz_id (str): Reference to the parent Quiz document.
        question_text (str): The question prompt shown to the user.
        question_type (str): Category (e.g. multiple_choice, scenario).
        options (List[str]): List of answer option strings.
        correct_index (int): Zero-based index of the correct option.
        explanation (str): Explanation shown after the user answers.
        order (int): Position within the parent quiz.
    """

    quiz_id: str
    question_text: str
    question_type: str = "multiple_choice"
    options: List[str] = Field(default_factory=list)
    correct_index: int = 0
    explanation: str = ""
    order: int = 0

    class Settings:
        name = "quiz_questions"


class Quiz(Document):
    """MongoDB document representing a quiz linked to a module or task.

    Attributes:
        module_id (str): Associated module ID.
        task_id (Optional[str]): Optional associated task ID.
        title (str): Human-readable quiz title.
        description (str): Short description shown before starting.
        passing_score (float): Minimum percentage required to pass.
        xp_reward (int): XP awarded on passing.
    """

    module_id: str
    task_id: Optional[str] = None
    title: str
    description: str = ""
    passing_score: float = 70.0
    xp_reward: int = 50

    class Settings:
        name = "quizzes"


class QuizAttemptAnswer(BaseModel):
    """Embedded model recording a single answer within an attempt.

    Attributes:
        question_id (str): ID of the QuizQuestion answered.
        selected_index (int): Zero-based index the user selected.
        is_correct (bool): Whether the answer was correct.
    """

    question_id: str
    selected_index: int
    is_correct: bool


class QuizAttempt(Document):
    """MongoDB document recording a user's attempt at a quiz.

    Attributes:
        user_id (str): ID of the user.
        quiz_id (str): ID of the attempted Quiz.
        answers (List[QuizAttemptAnswer]): List of per-question answer records.
        score (float): Percentage score achieved.
        passed (bool): Whether the score met the passing threshold.
        attempted_at (datetime): UTC timestamp of the attempt.
    """

    user_id: str
    quiz_id: str
    answers: List[QuizAttemptAnswer] = Field(default_factory=list)
    score: float = 0.0
    passed: bool = False
    attempted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "quiz_attempts"
