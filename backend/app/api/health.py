from fastapi import APIRouter

from app.config.settings import settings
from app.database.connection import get_connection

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    with get_connection() as connection:
        connection.execute("SELECT 1").fetchone()

    return {
        "status": "ok",
        "app": settings.app_name,
        "database": "connected",
    }
