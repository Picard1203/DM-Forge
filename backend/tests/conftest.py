"""Test configuration: async client, in-memory MongoDB, dependency overrides."""

import pytest_asyncio
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from src.main import app
from src.models.achievement import Achievement, UserAchievement
from src.models.curriculum import Module, Task
from src.models.progress import UserProgress
from src.models.quiz import Quiz, QuizAttempt
from src.models.review_card import ReviewCard, UserCardReview
from src.models.user import User
from src.repositories.mongodb.user_repository import MongoUserRepository
from src.services.auth_service import AuthService
from src.deps import get_auth_service
from src.utils.security import get_password_hash


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
            Quiz,
            QuizAttempt,
            Achievement,
            UserAchievement,
            ReviewCard,
            UserCardReview,
        ],
    )
    yield
    await User.find_all().delete()
    await Module.find_all().delete()
    await Task.find_all().delete()
    await UserProgress.find_all().delete()
    await Quiz.find_all().delete()
    await QuizAttempt.find_all().delete()
    await Achievement.find_all().delete()
    await UserAchievement.find_all().delete()
    await ReviewCard.find_all().delete()
    await UserCardReview.find_all().delete()


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
        email="hero@dmforge.com",
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
        json={"email": "hero@dmforge.com", "password": "Str0ngPass!"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def seeded_curriculum() -> dict:
    """Insert two test modules with tasks and return them keyed by slug.

    Returns:
        (dict): Mapping of module slug to inserted Module document.
    """
    module_alpha = Module(
        slug="rules-fundamentals",
        title="Rules Fundamentals",
        description="Core rules",
        order=1,
        estimated_hours=10,
        xp_reward=500,
        is_extension=False,
    )
    await module_alpha.insert()

    module_beta = Module(
        slug="narrative-tools",
        title="Narrative Tools",
        description="Storytelling techniques",
        order=2,
        estimated_hours=8,
        xp_reward=400,
        is_extension=False,
    )
    await module_beta.insert()

    task_one = Task(
        module_id=str(module_alpha.id),
        slug="rf-intro-video",
        title="Intro Video",
        description="Watch the intro",
        order=1,
        task_type="video",
        estimated_minutes=5,
        xp_reward=15,
        content={"youtube_url": "https://example.com/video1"},
    )
    await task_one.insert()

    task_two = Task(
        module_id=str(module_alpha.id),
        slug="rf-reading-phb",
        title="Read PHB p.4",
        description="Opening pages",
        order=2,
        task_type="reading",
        estimated_minutes=10,
        xp_reward=20,
        content={"book_title": "PHB", "page_start": 4, "page_end": 5},
    )
    await task_two.insert()

    return {
        "rules-fundamentals": module_alpha,
        "narrative-tools": module_beta,
        "task_one": task_one,
        "task_two": task_two,
    }
