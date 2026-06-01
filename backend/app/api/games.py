from fastapi import APIRouter, Query

from app.config.settings import settings
from app.database.schedule_repository import list_games
from app.models.schemas import GameResponse, GamesListResponse

router = APIRouter(tags=["games"])


@router.get("/games", response_model=GamesListResponse)
def get_games(season: str = Query(default=settings.nhl_default_season)) -> GamesListResponse:
    rows = list_games(int(season))
    games = [GameResponse(**row) for row in rows]

    return GamesListResponse(season=season, count=len(games), games=games)
