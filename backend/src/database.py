"""MongoDB connection and Beanie ODM initialisation."""

from typing import List

import motor.motor_asyncio
from beanie import Document, init_beanie

from src.config import settings
from src.models.achievement import Achievement, UserAchievement
from src.models.curriculum import Module, Task
from src.models.progress import UserProgress
from src.models.quiz import Quiz, QuizAttempt, QuizQuestion
from src.models.review_card import SpacedRepCard, UserCardReview
from src.models.user import User

_document_models: List[type[Document]] = [
    User,
    Module,
    Task,
    UserProgress,
    Quiz,
    QuizQuestion,
    QuizAttempt,
    Achievement,
    UserAchievement,
    SpacedRepCard,
    UserCardReview,
]


async def init_db() -> None:
    """Initialise Beanie with all Document models."""
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
    await init_beanie(database=client.get_database("dm_forge"), document_models=_document_models)
