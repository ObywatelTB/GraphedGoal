from fastapi import APIRouter
from .routes import goals_router

router = APIRouter()
router.include_router(goals_router)

__all__ = ["router"]
