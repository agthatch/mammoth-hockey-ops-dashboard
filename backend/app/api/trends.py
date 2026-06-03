from fastapi import APIRouter, HTTPException, Query

from app.analytics.trends import compute_trends
from app.config.settings import settings
from app.models.game_types import parse_game_type_query
from app.models.schemas import TrendGameResponse, TrendsResponse

router = APIRouter(tags=["trends"])


@router.get("/trends", response_model=TrendsResponse)
def get_trends(
    game_type: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1),
    season: str = Query(default=settings.nhl_default_season),
    team_abbr: str = Query(default=settings.nhl_team_abbr),
) -> TrendsResponse:
    try:
        game_type_code = parse_game_type_query(game_type)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    result = compute_trends(int(season), team_abbr, game_type_code, limit)

    return TrendsResponse(
        game_type=result.game_type,
        games=[
            TrendGameResponse(
                game_id=game.game_id,
                game_date=game.game_date,
                goals_for=game.goals_for,
                goals_against=game.goals_against,
                goal_differential=game.goal_differential,
                rolling_goals_for=game.rolling_goals_for,
                rolling_goals_against=game.rolling_goals_against,
                rolling_goal_differential=game.rolling_goal_differential,
            )
            for game in result.games
        ],
    )
