"""Quiz service: question serving, answer grading, and attempt storage."""

from typing import List, Optional

from src.models.quiz import Quiz, QuizAttempt, QuizAttemptAnswer, QuizQuestion
from src.repositories.abstract.quiz_repository import AbstractQuizRepository
from src.schemas.quiz import QuizResultResponse, SubmitAnswersRequest
from src.utils.exceptions import ResourceNotFoundError


class QuizService:
    """Handles quiz retrieval, grading, and attempt persistence.

    Attributes:
        _quiz_repository (AbstractQuizRepository): Injected repository for operations.
    """

    def __init__(self, quiz_repository: AbstractQuizRepository) -> None:
        """Initialise the service with a quiz repository.

        Args:
            quiz_repository (AbstractQuizRepository): Repository instance.
        """
        self._quiz_repository = quiz_repository

    async def get_quiz_with_questions(
        self, quiz_id: str
    ) -> tuple[Quiz, List[QuizQuestion]]:
        """Fetch a quiz and its ordered questions.

        Args:
            quiz_id (str): The quiz's document ID.

        Returns:
            tuple[Quiz, List[QuizQuestion]]: A tuple of (Quiz, questions).

        Raises:
            ResourceNotFoundError: If no quiz with that ID exists.
        """
        quiz: Optional[Quiz] = await self._quiz_repository.get_by_id(quiz_id)
        if quiz is None:
            raise ResourceNotFoundError("Quiz")
        questions = await self._quiz_repository.get_questions(quiz_id=quiz_id)
        return quiz, questions

    async def submit_answers(
        self, user_id: str, quiz_id: str, request: SubmitAnswersRequest
    ) -> QuizResultResponse:
        """Grade a quiz submission and persist the attempt.

        Args:
            user_id (str): The ID of the submitting user.
            quiz_id (str): The quiz's document ID.
            request (SubmitAnswersRequest): The answer submissions.

        Returns:
            QuizResultResponse: Result with score, pass status, and XP.

        Raises:
            ResourceNotFoundError: If the quiz does not exist.
        """
        quiz, questions = await self.get_quiz_with_questions(quiz_id=quiz_id)
        question_map: dict[str, QuizQuestion] = {}
        for question in questions:
            question_map[str(question.id)] = question
        answers: List[QuizAttemptAnswer] = []
        correct_count = 0
        for item in request.answers:
            question = question_map.get(item.question_id)
            is_correct = (
                question is not None and question.correct_index == item.selected_index
            )
            if is_correct is True:
                correct_count += 1
            answers.append(
                QuizAttemptAnswer(
                    question_id=item.question_id,
                    selected_index=item.selected_index,
                    is_correct=is_correct,
                )
            )
        total = len(questions)
        score = (correct_count / total * 100) if total > 0 else 0.0
        passed = score >= quiz.passing_score
        already_passed = await self._quiz_repository.has_passed(
            user_id=user_id, quiz_id=quiz_id
        )
        xp_awarded = quiz.xp_reward if (passed is True and already_passed is False) else 0
        attempt = QuizAttempt(
            user_id=user_id,
            quiz_id=quiz_id,
            answers=answers,
            score=score,
            passed=passed,
        )
        await self._quiz_repository.save_attempt(attempt)
        return QuizResultResponse(
            score=score,
            passed=passed,
            xp_awarded=xp_awarded,
            correct_count=correct_count,
            total_count=total,
        )
