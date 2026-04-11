"""MongoDB connection and Beanie ODM initialisation."""

from typing import List

import motor.motor_asyncio
from beanie import Document, init_beanie

from app.config import settings
from app.models.achievement import Achievement, UserAchievement
from app.models.curriculum import Module, Task
from app.models.progress import TaskCompletion, UserProgress
from app.models.quiz import Quiz, QuizAttempt, QuizQuestion
from app.models.review_card import SpacedRepCard, UserCardReview
from app.models.user import User

_document_models: List[type[Document]] = [
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
]


async def init_db() -> None:
    """Initialise Beanie with all Document models.

    Creates the async Motor client and calls beanie.init_beanie so that all
    Document subclasses are bound to the correct MongoDB collections.
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
    await init_beanie(database=client.get_default_database(), document_models=_document_models)
