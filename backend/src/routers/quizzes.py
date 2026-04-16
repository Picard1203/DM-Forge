"""Quizzes router: quiz retrieval and answer submission endpoints."""

from fastapi import APIRouter, Depends

from src.deps import get_current_user, get_quiz_service
from src.models.user import User
from src.schemas.quiz import QuizResponse, QuizResultResponse, SubmitQuizRequest
from src.services.quiz_service import QuizService

router = APIRouter(prefix="/api/v1/quizzes", tags=["quizzes"])


@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(
    quiz_id: str,
    _current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
) -> QuizResponse:
    """Return a quiz with its questions (correct answers hidden).

    Args:
        quiz_id (str): The quiz's document ID.
        _current_user (User): Authenticated user (access guard).
        quiz_service (QuizService): Injected service instance.

    Returns:
        QuizResponse: A QuizResponse with embedded questions.
    """
    return await quiz_service.get_quiz(quiz_id=quiz_id)


@router.post("/{quiz_id}/submit", response_model=QuizResultResponse)
async def submit_quiz(
    quiz_id: str,
    request: SubmitQuizRequest,
    current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
) -> QuizResultResponse:
    """Submit answers for a quiz and receive a graded result.

    Args:
        quiz_id (str): The quiz's document ID.
        request (SubmitQuizRequest): One answer index per question in order.
        current_user (User): The authenticated user.
        quiz_service (QuizService): Injected service instance.

    Returns:
        QuizResultResponse: Result with score, pass status, XP earned, and per-question breakdown.
    """
    return await quiz_service.submit_quiz(
        user=current_user,
        quiz_id=quiz_id,
        request=request,
    )
