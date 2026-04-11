"""Test configuration: async client, in-memory MongoDB, dependency overrides."""

import pytest
import pytest_asyncio
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.main import app
from app.models.achievement import Achievement, UserAchievement
from app.models.curriculum import Module, Task
from app.models.progress import TaskCompletion, UserProgress
from app.models.quiz import Quiz, QuizAttempt, QuizQuestion
from app.models.review_card import SpacedRepCard, UserCardReview
from app.models.user import User
from app.repositories.mongodb.user_repository import MongoUserRepository
from app.services.auth_service import AuthService
from app.deps import get_auth_service
from app.utils.security import get_password_hash


@pytest_asyncio.fixture(autouse=True)
async def init_test_db():
    """Initialise an in-memory Beanie database before each test."""
    client = AsyncMongoMockClient()
    await init_beanie(
        database=client["test_db"],
        document_models=[
            User,
            Module,
            Task,
            UserProgress,
            TaskCompletion,
            Quiz,
            QuizQuestion,
            QuizAttempt,
            Achievement,
            UserAchievement,
            SpacedRepCard,
            UserCardReview,
        ],
    )
    yield
    await User.find_all().delete()


def _override_auth_service() -> AuthService:
    """Return an AuthService backed by the in-memory user repository."""
    return AuthService(user_repository=MongoUserRepository())


app.dependency_overrides[get_auth_service] = _override_auth_service


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    """Provide an AsyncClient wired to the FastAPI test app."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def mock_user() -> User:
    """Insert and return a pre-registered test user."""
    user = User(
        email="hero@dmforge.test",
        username="HeroUser",
        hashed_password=get_password_hash("Str0ngPass!"),
    )
    await user.insert()
    return user


@pytest_asyncio.fixture
async def auth_token(client: AsyncClient, mock_user: User) -> str:
    """Return a valid JWT for the mock user by calling the login endpoint."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "hero@dmforge.test", "password": "Str0ngPass!"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]
