from fastapi import APIRouter, Query

from app.config.settings import settings
from app.database.season_sync_repository import get_season_sync
from app.models.schemas import SeasonStatusResponse

router = APIRouter(tags=["seasons"])


@router.get("/season-status", response_model=SeasonStatusResponse)
def get_season_status(
    season: str = Query(...),
    team_abbr: str = Query(default=settings.nhl_team_abbr),
) -> SeasonStatusResponse:
    row = get_season_sync(team_abbr, season)
    if row is None:
        return SeasonStatusResponse(
            season=season,
            team_abbr=team_abbr,
            last_sync_at=None,
            game_count=0,
        )

    return SeasonStatusResponse(
        season=season,
        team_abbr=team_abbr,
        last_sync_at=row["last_sync_at"],
        game_count=row["game_count"],
    )
