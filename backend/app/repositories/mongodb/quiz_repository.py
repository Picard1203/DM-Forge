"""MongoDB implementation of the AbstractQuizRepository."""

from typing import List, Optional

from beanie import PydanticObjectId

from app.models.quiz import Quiz, QuizAttempt, QuizQuestion
from app.repositories.abstract.quiz_repository import AbstractQuizRepository


class MongoQuizRepository(AbstractQuizRepository):
    """Concrete MongoDB repository for Quiz documents using Beanie ODM."""

    async def get_by_id(self, quiz_id: str) -> Optional[Quiz]:
        """Fetch a quiz by its document ID.

        Args:
            quiz_id: String representation of the MongoDB ObjectId.

        Returns:
            The matching Quiz document, or None if not found.
        """
        return await Quiz.get(PydanticObjectId(quiz_id))

    async def get_questions(self, quiz_id: str) -> List[QuizQuestion]:
        """Fetch all questions for a quiz, ordered by ``order`` ascending.

        Args:
            quiz_id: The parent quiz's document ID.

        Returns:
            Ordered list of QuizQuestion documents.
        """
        return await QuizQuestion.find(
            QuizQuestion.quiz_id == quiz_id
        ).sort(+QuizQuestion.order).to_list()

    async def save_attempt(self, attempt: QuizAttempt) -> QuizAttempt:
        """Persist a new quiz attempt.

        Args:
            attempt: The QuizAttempt document to insert.

        Returns:
            The persisted QuizAttempt with its assigned ID.
        """
        await attempt.insert()
        return attempt

    async def get_attempts(self, user_id: str, quiz_id: str) -> List[QuizAttempt]:
        """Fetch all attempts a user has made on a specific quiz.

        Args:
            user_id: The user's document ID.
            quiz_id: The quiz's document ID.

        Returns:
            List of QuizAttempt documents, most recent first.
        """
        return await QuizAttempt.find(
            QuizAttempt.user_id == user_id,
            QuizAttempt.quiz_id == quiz_id,
        ).sort(-QuizAttempt.attempted_at).to_list()

    async def has_passed(self, user_id: str, quiz_id: str) -> bool:
        """Check whether a user has ever passed a specific quiz.

        Args:
            user_id: The user's document ID.
            quiz_id: The quiz's document ID.

        Returns:
            True if at least one passing attempt exists.
        """
        passing = await QuizAttempt.find_one(
            QuizAttempt.user_id == user_id,
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.passed == True,
        )
        return passing is not None
