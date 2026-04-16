"""Pydantic schemas for quiz endpoints."""

from typing import List, Optional

from pydantic import BaseModel

from src.schemas.achievement import AchievementResponse


class QuizQuestionResponse(BaseModel):
    """Serialised quiz question with options shown and correct answer hidden.

    Attributes:
        id (str): Zero-based question index as a string (used as React key).
        question_text (str): The question prompt.
        question_type (str): Category of question (multiple_choice or scenario).
        options (List[str]): List of answer options.
        scenario_context (Optional[str]): Optional context paragraph for scenario questions.
    """

    id: str
    question_text: str
    question_type: str
    options: List[str]
    scenario_context: Optional[str] = None


class QuizResponse(BaseModel):
    """Serialised Quiz with embedded questions (correct answers stripped).

    Attributes:
        id (str): MongoDB document ID.
        slug (str): URL-friendly quiz identifier.
        title (str): Quiz display title.
        questions (List[QuizQuestionResponse]): Ordered list of questions.
    """

    id: str
    slug: str
    title: str
    questions: List[QuizQuestionResponse]


class SubmitQuizRequest(BaseModel):
    """Request body for submitting a completed quiz.

    Attributes:
        answers (List[int]): One selected answer index per question, in question order.
    """

    answers: List[int]


class QuizQuestionResult(BaseModel):
    """Per-question grading result returned after a quiz submission.

    Attributes:
        question_index (int): Zero-based position of the question.
        correct (bool): Whether the submitted answer was correct.
        correct_answer_index (int): The index of the correct answer.
        explanation (str): Explanation text shown after answering.
    """

    question_index: int
    correct: bool
    correct_answer_index: int
    explanation: str


class QuizResultResponse(BaseModel):
    """Result returned after grading a quiz attempt.

    Attributes:
        score (float): Fraction of questions correct (0.0–1.0).
        passed (bool): Whether the score met the passing threshold.
        xp_earned (int): XP granted (non-zero on first passing attempt only).
        already_completed (bool): True if the user has previously passed this quiz.
        question_results (List[QuizQuestionResult]): Per-question breakdown.
        earned_achievements (List[AchievementResponse]): Achievements unlocked by this attempt.
    """

    score: float
    passed: bool
    xp_earned: int
    already_completed: bool
    question_results: List[QuizQuestionResult]
    earned_achievements: List[AchievementResponse] = []
