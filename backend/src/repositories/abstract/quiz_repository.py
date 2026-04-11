"""Abstract repository interface for the Quiz domain."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.quiz import Quiz, QuizAttempt, QuizQuestion


class AbstractQuizRepository(ABC):
    """Abstract contract for quiz data persistence operations."""

    @abstractmethod
    async def get_by_id(self, quiz_id: str) -> Optional[Quiz]:
        """Fetch a quiz by its document ID.

        Args:
            quiz_id: String representation of the MongoDB ObjectId.

        Returns:
            The matching Quiz document, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_questions(self, quiz_id: str) -> List[QuizQuestion]:
        """Fetch all questions for a quiz, ordered by ``order`` ascending.

        Args:
            quiz_id: The parent quiz's document ID.

        Returns:
            Ordered list of QuizQuestion documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def save_attempt(self, attempt: QuizAttempt) -> QuizAttempt:
        """Persist a new quiz attempt.

        Args:
            attempt: The QuizAttempt document to insert.

        Returns:
            The persisted QuizAttempt with its assigned ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_attempts(self, user_id: str, quiz_id: str) -> List[QuizAttempt]:
        """Fetch all attempts a user has made on a specific quiz.

        Args:
            user_id: The user's document ID.
            quiz_id: The quiz's document ID.

        Returns:
            List of QuizAttempt documents, most recent first.
        """
        raise NotImplementedError

    @abstractmethod
    async def has_passed(self, user_id: str, quiz_id: str) -> bool:
        """Check whether a user has ever passed a specific quiz.

        Args:
            user_id: The user's document ID.
            quiz_id: The quiz's document ID.

        Returns:
            True if at least one passing attempt exists.
        """
        raise NotImplementedError
