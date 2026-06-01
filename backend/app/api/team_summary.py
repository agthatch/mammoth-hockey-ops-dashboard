from fastapi import APIRouter, HTTPException, Query

from app.analytics.team_summary import compute_team_summary
from app.config.settings import settings
from app.models.game_types import GameTypeCode, parse_game_type_query
from app.models.schemas import TeamSummaryResponse

router = APIRouter(tags=["team-summary"])


@router.get("/team-summary", response_model=TeamSummaryResponse)
def get_team_summary(
    season: str = Query(default=settings.nhl_default_season),
    game_type: str | None = Query(default=None),
    team_abbr: str = Query(default=settings.nhl_team_abbr),
) -> TeamSummaryResponse:
    try:
        game_type_code = parse_game_type_query(game_type)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    result = compute_team_summary(int(season), team_abbr, game_type_code)

    return TeamSummaryResponse(
        season=season,
        game_type=game_type_code.value,
        games_played=result.games_played,
        wins=result.wins,
        losses=result.losses,
        ot_losses=result.ot_losses,
        points=result.points,
        goals_for=result.goals_for,
        goals_against=result.goals_against,
        goal_differential=result.goal_differential,
    )
