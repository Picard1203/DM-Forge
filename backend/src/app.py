"""FastAPI application factory."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.database import init_db
from src.routers import achievements, auth, curriculum, progress, quizzes, review, sessions, users


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan: initialise DB on startup, clean up on shutdown.

    Args:
        application (FastAPI): The FastAPI application instance.

    Yields:
        None: Control is yielded to the running application.
    """
    await init_db()
    yield


def register_middleware(application: FastAPI) -> None:
    """Attach middleware to the application.

    Args:
        application (FastAPI): The FastAPI application instance to configure.
    """
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:80"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_routers(application: FastAPI) -> None:
    """Include all domain routers under the application.

    Args:
        application (FastAPI): The FastAPI application instance to configure.
    """
    application.include_router(auth.router)
    application.include_router(users.router)
    application.include_router(curriculum.router)
    application.include_router(progress.router)
    application.include_router(quizzes.router)
    application.include_router(sessions.router)
    application.include_router(achievements.router)
    application.include_router(review.router)


def register_exception_handlers(application: FastAPI) -> None:
    """Register custom exception handlers on the application.

    Args:
        application (FastAPI): The FastAPI application instance to configure.
    """

    @application.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Handle all HTTPExceptions by returning a structured JSON response.

        Args:
            request (Request): The incoming HTTP request.
            exc (HTTPException): The raised HTTP exception.

        Returns:
            JSONResponse: A formatted JSON response with the error detail.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )


def create_app() -> FastAPI:
    """Construct, configure, and return the FastAPI application.

    Returns:
        FastAPI: A fully configured application instance ready to serve.
    """
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    register_middleware(application)
    register_routers(application)
    register_exception_handlers(application)
    return application
