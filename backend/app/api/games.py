from fastapi import APIRouter, HTTPException, Query

from app.database.schedule_repository import list_games
from app.models.schemas import GameResponse, GamesListResponse
from app.models.seasons import DEFAULT_SEASON_ID, parse_season_query, season_to_int

router = APIRouter(tags=["games"])


@router.get("/games", response_model=GamesListResponse)
def get_games(season: str = Query(default=DEFAULT_SEASON_ID)) -> GamesListResponse:
    try:
        season_id = parse_season_query(season)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    rows = list_games(season_to_int(season_id))
    games = [GameResponse(**row) for row in rows]

    return GamesListResponse(season=season_id, count=len(games), games=games)
