"""ASGI entry point for the GraphedGoal backend."""

from backend.app.main import app

# This file can be referenced by uvicorn directly:
# uvicorn backend.asgi:app --reload
