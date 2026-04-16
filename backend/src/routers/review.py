"""Review router: spaced repetition due cards and submission endpoints."""

from typing import List

from fastapi import APIRouter, Depends

from src.deps import get_current_user, get_review_service
from src.models.user import User
from src.schemas.review import ReviewCardResponse, ReviewSubmitRequest, ReviewSubmitResponse
from src.services.review_service import ReviewService

router = APIRouter(prefix="/api/v1/review", tags=["review"])


@router.get("/due", response_model=List[ReviewCardResponse])
async def get_due_cards(
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> List[ReviewCardResponse]:
    """Return flashcards due for review for the authenticated user.

    Args:
        current_user (User): The authenticated user.
        review_service (ReviewService): Injected service instance.

    Returns:
        List[ReviewCardResponse]: Cards due for review (overdue or never reviewed).
    """
    return await review_service.get_due_cards(user_id=str(current_user.id))


@router.post("/submit", response_model=ReviewSubmitResponse)
async def submit_review(
    request: ReviewSubmitRequest,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> ReviewSubmitResponse:
    """Submit a quality rating for a reviewed flashcard.

    Args:
        request (ReviewSubmitRequest): Contains card_id and quality rating (0–5).
        current_user (User): The authenticated user.
        review_service (ReviewService): Injected service instance.

    Returns:
        ReviewSubmitResponse: Updated schedule with next_review date and interval.
    """
    return await review_service.submit_review(
        user_id=str(current_user.id), request=request
    )
