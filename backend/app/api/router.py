from fastapi import APIRouter

from app.api.games import router as games_router
from app.api.health import router as health_router
from app.api.ingest import router as ingest_router
from app.api.team_summary import router as team_summary_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(ingest_router)
api_router.include_router(games_router)
api_router.include_router(team_summary_router)
