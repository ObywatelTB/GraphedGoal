from fastapi import APIRouter
from .goals import router as goals_router

api_router = APIRouter()

api_router.include_router(goals_router, prefix="/goals", tags=["goals"])
