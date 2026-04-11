"""Quizzes router: quiz retrieval and answer submission endpoints."""

from fastapi import APIRouter, Depends

from src.deps import get_current_user, get_quiz_service
from src.models.user import User
from src.schemas.quiz import QuizResponse, QuizQuestionResponse, QuizResultResponse, SubmitAnswersRequest
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
        quiz_id: The quiz's document ID.
        _current_user: Authenticated user (access guard).
        quiz_service: Injected QuizService instance.

    Returns:
        A QuizResponse with embedded questions.
    """
    quiz, questions = await quiz_service.get_quiz_with_questions(quiz_id)
    return QuizResponse(
        id=str(quiz.id),
        module_id=quiz.module_id,
        title=quiz.title,
        description=quiz.description,
        passing_score=quiz.passing_score,
        xp_reward=quiz.xp_reward,
        questions=[
            QuizQuestionResponse(
                id=str(q.id),
                question_text=q.question_text,
                question_type=q.question_type,
                options=q.options,
                order=q.order,
            )
            for q in questions
        ],
    )


@router.post("/{quiz_id}/submit", response_model=QuizResultResponse)
async def submit_quiz(
    quiz_id: str,
    request: SubmitAnswersRequest,
    current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
) -> QuizResultResponse:
    """Submit answers for a quiz and receive a graded result.

    Args:
        quiz_id: The quiz's document ID.
        request: The list of question-answer pairs.
        current_user: The authenticated user.
        quiz_service: Injected QuizService instance.

    Returns:
        A QuizResultResponse with score, pass status, and XP awarded.
    """
    return await quiz_service.submit_answers(
        user_id=str(current_user.id),
        quiz_id=quiz_id,
        request=request,
    )
