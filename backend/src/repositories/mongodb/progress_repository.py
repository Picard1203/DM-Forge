"""MongoDB implementation of the AbstractProgressRepository."""

from typing import List, Optional

from src.models.progress import UserProgress
from src.repositories.abstract.progress_repository import AbstractProgressRepository


class MongoProgressRepository(AbstractProgressRepository):
    """Concrete MongoDB repository for progress tracking using Beanie ODM."""

    async def get_by_user_and_task(
        self, user_id: str, task_id: str
    ) -> Optional[UserProgress]:
        """Fetch the progress record for a specific user-task pair.

        Args:
            user_id (str): The user's document ID.
            task_id (str): The task's document ID.

        Returns:
            Optional[UserProgress]: The matching document, or None if not found.
        """
        return await UserProgress.find_one(
            UserProgress.user_id == user_id,
            UserProgress.task_id == task_id,
        )

    async def get_by_user_and_module(
        self, user_id: str, module_id: str
    ) -> List[UserProgress]:
        """Fetch all progress records for a user within a specific module.

        Args:
            user_id (str): The user's document ID.
            module_id (str): The module's document ID.

        Returns:
            List[UserProgress]: All UserProgress documents for that module.
        """
        return await UserProgress.find(
            UserProgress.user_id == user_id,
            UserProgress.module_id == module_id,
        ).to_list()

    async def get_all_for_user(self, user_id: str) -> List[UserProgress]:
        """Fetch every progress record belonging to a user across all modules.

        Args:
            user_id (str): The user's document ID.

        Returns:
            List[UserProgress]: All UserProgress documents for the user.
        """
        return await UserProgress.find(
            UserProgress.user_id == user_id
        ).to_list()

    async def create(self, progress: UserProgress) -> UserProgress:
        """Persist a new UserProgress document.

        Args:
            progress (UserProgress): The document instance to insert.

        Returns:
            UserProgress: The persisted document with its assigned ID.
        """
        await progress.insert()
        return progress
