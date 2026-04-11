"""Composition root — the only module that imports MongoDB concrete implementations.

All FastAPI dependency functions are defined here. Services are constructed by
injecting the appropriate concrete repository implementations.
"""

from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.models.user import User
from src.repositories.mongodb.achievement_repository import MongoAchievementRepository
from src.repositories.mongodb.module_repository import MongoModuleRepository
from src.repositories.mongodb.progress_repository import MongoProgressRepository
from src.repositories.mongodb.quiz_repository import MongoQuizRepository
from src.repositories.mongodb.review_card_repository import MongoReviewCardRepository
from src.repositories.mongodb.task_repository import MongoTaskRepository
from src.repositories.mongodb.user_repository import MongoUserRepository
from src.services.achievement_service import AchievementService
from src.services.auth_service import AuthService
from src.services.curriculum_service import CurriculumService
from src.services.gamification_service import GamificationService
from src.services.progress_service import ProgressService
from src.services.quiz_service import QuizService
from src.services.review_service import ReviewService
from src.services.session_service import SessionService
from src.services.user_service import UserService
from src.utils.exceptions import InvalidCredentialsError

_bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_service() -> AuthService:
    """Construct an AuthService with a MongoDB user repository.

    Returns:
        Fully wired AuthService instance.
    """
    return AuthService(user_repository=MongoUserRepository())


def get_user_service() -> UserService:
    """Construct a UserService with a MongoDB user repository.

    Returns:
        Fully wired UserService instance.
    """
    return UserService(user_repository=MongoUserRepository())


def get_curriculum_service() -> CurriculumService:
    """Construct a CurriculumService with MongoDB repositories.

    Returns:
        Fully wired CurriculumService instance.
    """
    return CurriculumService(
        module_repository=MongoModuleRepository(),
        task_repository=MongoTaskRepository(),
    )


def get_progress_service() -> ProgressService:
    """Construct a ProgressService with MongoDB repositories.

    Returns:
        Fully wired ProgressService instance.
    """
    return ProgressService(
        progress_repository=MongoProgressRepository(),
        task_repository=MongoTaskRepository(),
    )


def get_quiz_service() -> QuizService:
    """Construct a QuizService with MongoDB repositories.

    Returns:
        Fully wired QuizService instance.
    """
    return QuizService(quiz_repository=MongoQuizRepository())


def get_session_service() -> SessionService:
    """Construct a SessionService with required dependencies.

    Returns:
        Fully wired SessionService instance.
    """
    return SessionService(
        curriculum_service=get_curriculum_service(),
        progress_service=get_progress_service(),
    )


def get_achievement_service() -> AchievementService:
    """Construct an AchievementService with MongoDB repositories.

    Returns:
        Fully wired AchievementService instance.
    """
    return AchievementService(achievement_repository=MongoAchievementRepository())


def get_gamification_service() -> GamificationService:
    """Construct a GamificationService with required dependencies.

    Returns:
        Fully wired GamificationService instance.
    """
    return GamificationService(
        user_repository=MongoUserRepository(),
        achievement_service=get_achievement_service(),
    )


def get_review_service() -> ReviewService:
    """Construct a ReviewService with MongoDB repositories.

    Returns:
        Fully wired ReviewService instance.
    """
    return ReviewService(review_card_repository=MongoReviewCardRepository())


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Extract and validate the current user from the Bearer token.

    Args:
        credentials: HTTP Authorization header credentials.
        auth_service: Injected AuthService instance.

    Returns:
        The authenticated User document.

    Raises:
        InvalidCredentialsError: If the token is missing, invalid, or the user
            is not found.
    """
    if credentials is None:
        raise InvalidCredentialsError()
    return await auth_service.get_current_user(token=credentials.credentials)
