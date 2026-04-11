"""Pydantic schemas for quiz endpoints."""

from typing import List

from pydantic import BaseModel


class QuizQuestionResponse(BaseModel):
    """Serialised quiz question (options shown, correct answer hidden).

    Attributes:
        id (str): MongoDB document ID.
        question_text (str): The question prompt.
        question_type (str): Category of question.
        options (List[str]): List of answer options.
        order (int): Position within the quiz.
    """

    id: str
    question_text: str
    question_type: str
    options: List[str]
    order: int


class QuizResponse(BaseModel):
    """Serialised Quiz with embedded questions.

    Attributes:
        id (str): MongoDB document ID.
        module_id (str): Associated module ID.
        title (str): Quiz display title.
        description (str): Pre-quiz description.
        passing_score (float): Minimum pass percentage.
        xp_reward (int): XP awarded on pass.
        questions (List[QuizQuestionResponse]): Ordered list of questions.
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
        question_id (str): ID of the question answered.
        selected_index (int): Zero-based index of the chosen option.
    """

    question_id: str
    selected_index: int


class SubmitAnswersRequest(BaseModel):
    """Request body for submitting a completed quiz.

    Attributes:
        answers (List[SubmitAnswerItem]): List of answer submissions.
    """

    answers: List[SubmitAnswerItem]


class QuizResultResponse(BaseModel):
    """Result returned after grading a quiz attempt.

    Attributes:
        score (float): Percentage score achieved.
        passed (bool): Whether the score met the passing threshold.
        xp_awarded (int): XP granted (non-zero on first pass).
        correct_count (int): Number of correctly answered questions.
        total_count (int): Total number of questions.
    """

    score: float
    passed: bool
    xp_awarded: int
    correct_count: int
    total_count: int
