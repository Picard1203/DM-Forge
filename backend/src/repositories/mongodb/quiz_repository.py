"""MongoDB implementation of the AbstractQuizRepository."""

from typing import List, Optional

from beanie import PydanticObjectId

from src.models.quiz import Quiz, QuizAttempt
from src.repositories.abstract.quiz_repository import AbstractQuizRepository


class MongoQuizRepository(AbstractQuizRepository):
    """Concrete MongoDB repository for Quiz documents using Beanie ODM."""

    async def get_by_id(self, quiz_id: str) -> Optional[Quiz]:
        """Fetch a quiz by its document ID.

        Args:
            quiz_id (str): String representation of the MongoDB ObjectId.

        Returns:
            Optional[Quiz]: The matching Quiz document, or None if not found.
        """
        return await Quiz.get(PydanticObjectId(quiz_id))

    async def get_by_slug(self, slug: str) -> Optional[Quiz]:
        """Fetch a quiz by its slug.

        Args:
            slug (str): The unique slug identifier.

        Returns:
            Optional[Quiz]: The matching Quiz document, or None if not found.
        """
        return await Quiz.find_one(Quiz.slug == slug)

    async def get_by_module_id(self, module_id: str) -> List[Quiz]:
        """Fetch all quizzes associated with a module.

        Args:
            module_id (str): The module's document ID.

        Returns:
            List[Quiz]: All Quiz documents for that module.
        """
        return await Quiz.find(Quiz.module_id == module_id).to_list()

    async def save_attempt(self, attempt: QuizAttempt) -> QuizAttempt:
        """Persist a new quiz attempt.

        Args:
            attempt (QuizAttempt): The QuizAttempt document to insert.

        Returns:
            QuizAttempt: The persisted QuizAttempt with its assigned ID.
        """
        await attempt.insert()
        return attempt

    async def get_attempts_for_user(self, user_id: str, quiz_id: str) -> List[QuizAttempt]:
        """Fetch all attempts a user has made on a specific quiz.

        Args:
            user_id (str): The user's document ID.
            quiz_id (str): The quiz's document ID.

        Returns:
            List[QuizAttempt]: List of QuizAttempt documents.
        """
        return await QuizAttempt.find(
            QuizAttempt.user_id == user_id,
            QuizAttempt.quiz_id == quiz_id,
        ).to_list()
