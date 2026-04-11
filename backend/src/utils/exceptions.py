"""Custom HTTP exceptions for the DM Forge API."""

from fastapi import HTTPException, status


class EmailAlreadyExistsError(HTTPException):
    """Raised when registration is attempted with an already-registered email.

    Attributes:
        status_code: HTTP 409 Conflict.

    """

    def __init__(self) -> None:
        """Initialise with a fixed 409 status and descriptive detail."""
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists.",
        )


class UsernameAlreadyExistsError(HTTPException):
    """Raised when registration is attempted with an already-taken username.

    Attributes:
        status_code: HTTP 409 Conflict.

    """

    def __init__(self) -> None:
        """Initialise with a fixed 409 status and descriptive detail."""
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is already taken.",
        )


class InvalidCredentialsError(HTTPException):
    """Raised when authentication fails due to bad credentials or a missing token.

    Attributes:
        status_code: HTTP 401 Unauthorized.

    """

    def __init__(self) -> None:
        """Initialise with a fixed 401 status and descriptive detail."""
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserNotFoundError(HTTPException):
    """Raised when a requested user cannot be located in the database.

    Attributes:
        status_code: HTTP 404 Not Found.

    """

    def __init__(self) -> None:
        """Initialise with a fixed 404 status and descriptive detail."""
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )


class ResourceNotFoundError(HTTPException):
    """Generic 404 for any resource that cannot be located.

    Attributes:
        status_code: HTTP 404 Not Found.

    """

    def __init__(self, resource: str = "Resource") -> None:
        """Initialise with a fixed 404 status and descriptive detail.

        Args:
            resource: Human-readable name of the missing resource.

        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found.",
        )


class ForbiddenError(HTTPException):
    """Raised when a user attempts to access a resource they do not own.

    Attributes:
        status_code: HTTP 403 Forbidden.

    """

    def __init__(self) -> None:
        """Initialise with a fixed 403 status and descriptive detail."""
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
