"""Composition root — the only module that imports MongoDB concrete implementations."""

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
        AuthService: Fully wired AuthService instance.

    """
    return AuthService(user_repository=MongoUserRepository())


def get_user_service() -> UserService:
    """Construct a UserService with a MongoDB user repository.

    Returns:
        UserService: Fully wired UserService instance.

    """
    return UserService(user_repository=MongoUserRepository())


def get_curriculum_service() -> CurriculumService:
    """Construct a CurriculumService with MongoDB repositories.

    Returns:
        CurriculumService: Fully wired CurriculumService instance.

    """
    return CurriculumService(
        module_repository=MongoModuleRepository(),
        task_repository=MongoTaskRepository(),
    )


def get_gamification_service() -> GamificationService:
    """Construct a GamificationService with a MongoDB user repository.

    Returns:
        GamificationService: Fully wired GamificationService instance.

    """
    return GamificationService(user_repository=MongoUserRepository())


def get_progress_service() -> ProgressService:
    """Construct a ProgressService with MongoDB repositories and GamificationService.

    Returns:
        ProgressService: Fully wired ProgressService instance.

    """
    return ProgressService(
        progress_repository=MongoProgressRepository(),
        task_repository=MongoTaskRepository(),
        gamification_service=get_gamification_service(),
    )


def get_quiz_service() -> QuizService:
    """Construct a QuizService with MongoDB repositories.

    Returns:
        QuizService: Fully wired QuizService instance.

    """
    return QuizService(quiz_repository=MongoQuizRepository())


def get_session_service() -> SessionService:
    """Construct a SessionService with required repositories.

    Returns:
        SessionService: Fully wired SessionService instance.

    """
    return SessionService(
        module_repository=MongoModuleRepository(),
        task_repository=MongoTaskRepository(),
        progress_repository=MongoProgressRepository(),
    )


def get_achievement_service() -> AchievementService:
    """Construct an AchievementService with MongoDB repositories.

    Returns:
        AchievementService: Fully wired AchievementService instance.

    """
    return AchievementService(achievement_repository=MongoAchievementRepository())


def get_review_service() -> ReviewService:
    """Construct a ReviewService with MongoDB repositories.

    Returns:
        ReviewService: Fully wired ReviewService instance.

    """
    return ReviewService(review_card_repository=MongoReviewCardRepository())


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Extract and validate the current user from the Bearer token.

    Args:
        credentials (Optional[HTTPAuthorizationCredentials]): Bearer token credentials.
        auth_service (AuthService): Injected AuthService instance.

    Returns:
        User: The authenticated User document.

    Raises:
        InvalidCredentialsError: If token is missing, invalid, or user not found.

    """
    if credentials is None:
        raise InvalidCredentialsError()
    return await auth_service.get_current_user(token=credentials.credentials)
