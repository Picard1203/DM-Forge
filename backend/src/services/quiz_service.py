"""Quiz service: question serving, answer grading, and attempt storage."""

from typing import List, Optional       
from beanie import PydanticObjectId
from src.models.quiz import Quiz, QuizAttempt
from src.models.user import User
from src.repositories.abstract.quiz_repository import AbstractQuizRepository
from src.schemas.quiz import (
    QuizQuestionResponse,
    QuizQuestionResult,
    QuizResponse,
    QuizResultResponse,
    SubmitQuizRequest,
)
from src.services.gamification_service import GamificationService
from src.utils.exceptions import QuizNotFoundError


class QuizService:
    """Handles quiz retrieval, grading, and attempt persistence.

    Attributes:
        _quiz_repository (AbstractQuizRepository): Injected quiz repository.
        _gamification_service (GamificationService): Injected gamification service.
    """

    def __init__(
        self,
        quiz_repository: AbstractQuizRepository,
        gamification_service: GamificationService,
    ) -> None:
        """Initialise the service with required dependencies.

        Args:
            quiz_repository (AbstractQuizRepository): Quiz repository instance.
            gamification_service (GamificationService): Gamification service instance.
        """
        self._quiz_repository = quiz_repository
        self._gamification_service = gamification_service

    async def get_quiz(self, quiz_id: str) -> QuizResponse:
        """Fetch a quiz with questions, stripping correct answers and explanations.

        Args:
            quiz_id (str): The quiz's document ID or unique slug.

        Returns:
            QuizResponse: Quiz data safe to send to the client.

        Raises:
            QuizNotFoundError: If no quiz with that identifier exists.
        """
        quiz = await self._resolve_quiz(quiz_id)
        if quiz is None:
            raise QuizNotFoundError()
        return self._to_quiz_response(quiz)

    async def submit_quiz(
        self, user: User, quiz_id: str, request: SubmitQuizRequest
    ) -> QuizResultResponse:
        """Grade a quiz submission, award XP on first pass, and persist the attempt.

        Args:
            user (User): The authenticated user submitting the quiz.
            quiz_id (str): The quiz's document ID or unique slug.
            request (SubmitQuizRequest): Contains the list of selected answer indices.

        Returns:
            QuizResultResponse: Graded result with score, XP, and per-question breakdown.

        Raises:
            QuizNotFoundError: If the quiz does not exist.
        """
        quiz = await self._resolve_quiz(quiz_id)
        if quiz is None:
            raise QuizNotFoundError()

        # Always use the technical ObjectId for attempt linking
        resolved_quiz_id = str(quiz.id)

        question_results = self._grade_answers(quiz=quiz, answers=request.answers)
        correct_count = self._count_correct(question_results)
        total = len(quiz.questions)
        score = correct_count / total if total > 0 else 0.0
        passed = score >= quiz.passing_score
        already_completed = await self._has_prior_pass(
            user_id=str(user.id), quiz_id=resolved_quiz_id
        )
        xp_earned = quiz.xp_reward if (passed is True and already_completed is False) else 0
        if xp_earned > 0:
            await self._gamification_service.award_xp(user=user, xp_amount=xp_earned)
        attempt = QuizAttempt(
            user_id=str(user.id),
            quiz_id=resolved_quiz_id,
            answers=request.answers,
            score=score,
            passed=passed,
        )
        await self._quiz_repository.save_attempt(attempt)
        return QuizResultResponse(
            score=score,
            passed=passed,
            xp_earned=xp_earned,
            already_completed=already_completed,
            question_results=question_results,
            earned_achievements=[],
        )

    async def _resolve_quiz(self, identifier: str) -> Optional[Quiz]:
        """Helper to find a quiz by either technical ObjectId or human-readable slug.

        Args:
            identifier (str): The string to resolve.

        Returns:
            Optional[Quiz]: The found quiz or None.
        """
        if PydanticObjectId.is_valid(identifier):
            return await self._quiz_repository.get_by_id(identifier)
        return await self._quiz_repository.get_by_slug(identifier)

    def _to_quiz_response(self, quiz: Quiz) -> QuizResponse:
        """Convert a Quiz document to a client-safe QuizResponse.

        Args:
            quiz (Quiz): The Quiz document to convert.

        Returns:
            QuizResponse: Quiz response with questions stripped of answers.
        """
        question_responses: List[QuizQuestionResponse] = []
        for idx, question in enumerate(quiz.questions):
            question_responses.append(
                QuizQuestionResponse(
                    id=str(idx),
                    question_text=question.question_text,
                    question_type=question.question_type,
                    options=question.options,
                    scenario_context=question.scenario_context,
                )
            )
        return QuizResponse(
            id=str(quiz.id),
            slug=quiz.slug,
            title=quiz.title,
            questions=question_responses,
        )

    def _grade_answers(
        self, quiz: Quiz, answers: List[int]
    ) -> List[QuizQuestionResult]:
        """Compare submitted answers against correct answers for each question.

        Args:
            quiz (Quiz): The Quiz document containing embedded questions.
            answers (List[int]): One selected index per question, in question order.

        Returns:
            List[QuizQuestionResult]: Per-question grading results.
        """
        results: List[QuizQuestionResult] = []
        for idx, question in enumerate(quiz.questions):
            if idx < len(answers):
                selected = answers[idx]
            else:
                selected = -1
            is_correct = selected == question.correct_answer_index
            results.append(
                QuizQuestionResult(
                    question_index=idx,
                    correct=is_correct,
                    correct_answer_index=question.correct_answer_index,
                    explanation=question.explanation,
                )
            )
        return results

    def _count_correct(self, question_results: List[QuizQuestionResult]) -> int:
        """Count the number of correctly answered questions.

        Args:
            question_results (List[QuizQuestionResult]): Grading results per question.

        Returns:
            int: Number of results where correct is True.
        """
        count = 0
        for result in question_results:
            if result.correct is True:
                count += 1
        return count

    async def _has_prior_pass(self, user_id: str, quiz_id: str) -> bool:
        """Check whether the user has already passed this quiz.

        Args:
            user_id (str): The user's document ID.
            quiz_id (str): The quiz's document ID.

        Returns:
            bool: True if at least one prior passing attempt exists.
        """
        prior_attempts = await self._quiz_repository.get_attempts_for_user(
            user_id=user_id, quiz_id=quiz_id
        )
        found_pass = False
        for attempt in prior_attempts:
            if attempt.passed is True:
                found_pass = True
        return found_pass
