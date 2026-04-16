"""Abstract repository interface for the Quiz domain."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.quiz import Quiz, QuizAttempt


class AbstractQuizRepository(ABC):
    """Abstract contract for quiz data persistence operations."""

    @abstractmethod
    async def get_by_id(self, quiz_id: str) -> Optional[Quiz]:
        """Fetch a quiz by its document ID.

        Args:
            quiz_id (str): String representation of the MongoDB ObjectId.

        Returns:
            Optional[Quiz]: The matching Quiz document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Quiz]:
        """Fetch a quiz by its slug.

        Args:
            slug (str): The unique slug identifier.

        Returns:
            Optional[Quiz]: The matching Quiz document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_module_id(self, module_id: str) -> List[Quiz]:
        """Fetch all quizzes associated with a module.

        Args:
            module_id (str): The module's document ID.

        Returns:
            List[Quiz]: All Quiz documents for that module.
        """
        raise NotImplementedError

    @abstractmethod
    async def save_attempt(self, attempt: QuizAttempt) -> QuizAttempt:
        """Persist a new quiz attempt.

        Args:
            attempt (QuizAttempt): The QuizAttempt document to insert.

        Returns:
            QuizAttempt: The persisted QuizAttempt with its assigned ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_attempts_for_user(self, user_id: str, quiz_id: str) -> List[QuizAttempt]:
        """Fetch all attempts a user has made on a specific quiz.

        Args:
            user_id (str): The user's document ID.
            quiz_id (str): The quiz's document ID.

        Returns:
            List[QuizAttempt]: List of QuizAttempt documents.
        """
        raise NotImplementedError
