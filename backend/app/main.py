from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Try both relative and absolute imports
try:
    from app.core.config import settings
    from app.api import router as api_router
except ImportError:  # If running from within the app directory
    from core.config import settings
    from api import router as api_router


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API for goal visualization and planning",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Add root endpoint
    @app.get("/")
    async def root():
        return {"message": "Welcome to GraphedGoal API"}

    return app


app = create_application()
