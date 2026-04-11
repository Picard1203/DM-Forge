"""Pydantic schemas for quiz endpoints."""

from typing import List

from pydantic import BaseModel


class QuizQuestionResponse(BaseModel):
    """Serialised quiz question (options shown, correct answer hidden).

    Attributes:
        id: MongoDB document ID.
        question_text: The question prompt.
        question_type: Category of question.
        options: List of answer options.
        order: Position within the quiz.
    """

    id: str
    question_text: str
    question_type: str
    options: List[str]
    order: int


class QuizResponse(BaseModel):
    """Serialised Quiz with embedded questions.

    Attributes:
        id: MongoDB document ID.
        module_id: Associated module ID.
        title: Quiz display title.
        description: Pre-quiz description.
        passing_score: Minimum pass percentage.
        xp_reward: XP awarded on pass.
        questions: Ordered list of questions.
    """

    id: str
    module_id: str
    title: str
    description: str
    passing_score: float
    xp_reward: int
    questions: List[QuizQuestionResponse]


class SubmitAnswerItem(BaseModel):
    """Single answer submission within a quiz attempt.

    Attributes:
        question_id: ID of the question answered.
        selected_index: Zero-based index of the chosen option.
    """

    question_id: str
    selected_index: int


class SubmitAnswersRequest(BaseModel):
    """Request body for submitting a completed quiz.

    Attributes:
        answers: List of per-question answer submissions.
    """

    answers: List[SubmitAnswerItem]


class QuizResultResponse(BaseModel):
    """Result returned after grading a quiz attempt.

    Attributes:
        score: Percentage score achieved.
        passed: Whether the score met the passing threshold.
        xp_awarded: XP granted for this attempt (non-zero on first pass).
        correct_count: Number of correctly answered questions.
        total_count: Total number of questions.
    """

    score: float
    passed: bool
    xp_awarded: int
    correct_count: int
    total_count: int
