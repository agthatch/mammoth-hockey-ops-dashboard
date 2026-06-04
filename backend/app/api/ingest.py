from fastapi import APIRouter, HTTPException, Query

from app.config.settings import settings
from app.database.schedule_repository import save_schedule_snapshot, upsert_games
from app.database.season_sync_repository import upsert_season_sync
from app.models.schemas import IngestScheduleResponse
from app.services.nhl_service import NHLService, NHLServiceError

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/schedule", response_model=IngestScheduleResponse)
def ingest_schedule(
    season: str = Query(default=settings.nhl_default_season),
    team_abbr: str = Query(default=settings.nhl_team_abbr),
) -> IngestScheduleResponse:
    service = NHLService()

    try:
        schedule_data = service.fetch_schedule(season, team_abbr)
    except NHLServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    fetched_at = save_schedule_snapshot(team_abbr, season, schedule_data)
    games = schedule_data.get("games") or []
    games_ingested = upsert_games(games)
    upsert_season_sync(team_abbr, season, fetched_at, games_ingested)

    return IngestScheduleResponse(
        team_abbr=team_abbr,
        season=season,
        games_ingested=games_ingested,
        fetched_at=fetched_at,
    )
