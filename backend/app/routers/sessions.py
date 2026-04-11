"""Sessions router: time-aware session plan builder endpoint."""

from fastapi import APIRouter, Depends

from app.deps import get_current_user, get_session_service
from app.models.user import User
from app.schemas.session import SessionPlanResponse, SessionRequest
from app.services.session_service import SessionService

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


@router.post("/plan", response_model=SessionPlanResponse)
async def plan_session(
    request: SessionRequest,
    current_user: User = Depends(get_current_user),
    session_service: SessionService = Depends(get_session_service),
) -> SessionPlanResponse:
    """Generate a session plan fitting within the user's available time.

    Args:
        request: Contains the number of available minutes.
        current_user: The authenticated user.
        session_service: Injected SessionService instance.

    Returns:
        A SessionPlanResponse with an ordered task list.
    """
    return await session_service.build_plan(
        user_id=str(current_user.id), request=request
    )
