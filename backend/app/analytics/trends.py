"""Trend analytics computed from stored game data."""

from dataclasses import dataclass

import pandas as pd

from app.analytics.team_summary import _prepare_team_games
from app.database.schedule_repository import list_games
from app.models.game_types import GameTypeCode, to_nhl_game_type

ROLLING_WINDOW = 5


@dataclass(frozen=True)
class TrendGameResult:
    game_id: int
    game_date: str
    goals_for: int
    goals_against: int
    goal_differential: int
    rolling_goals_for: float
    rolling_goals_against: float
    rolling_goal_differential: float


@dataclass(frozen=True)
class TrendsResult:
    game_type: str
    games: list[TrendGameResult]


def _empty_trends(game_type: GameTypeCode) -> TrendsResult:
    return TrendsResult(game_type=game_type.value, games=[])


def _dataframe_to_trend_games(team_games: pd.DataFrame) -> list[TrendGameResult]:
    return [
        TrendGameResult(
            game_id=int(row.game_id),
            game_date=str(row.game_date),
            goals_for=int(row.goals_for),
            goals_against=int(row.goals_against),
            goal_differential=int(row.goal_differential),
            rolling_goals_for=float(row.rolling_goals_for),
            rolling_goals_against=float(row.rolling_goals_against),
            rolling_goal_differential=float(row.rolling_goal_differential),
        )
        for row in team_games.itertuples(index=False)
    ]


def compute_trends(
    season: int,
    team_abbr: str,
    game_type: GameTypeCode,
    limit: int = 20,
) -> TrendsResult:
    games = list_games(season=season, game_type=to_nhl_game_type(game_type))
    if not games:
        return _empty_trends(game_type)

    team_games = _prepare_team_games(pd.DataFrame(games), team_abbr)
    if team_games.empty:
        return _empty_trends(game_type)

    team_games = team_games.sort_values(["game_date", "start_time_utc"]).reset_index(drop=True)
    team_games = team_games.tail(limit).reset_index(drop=True)

    team_games["goal_differential"] = team_games["goals_for"] - team_games["goals_against"]
    team_games["rolling_goals_for"] = (
        team_games["goals_for"].rolling(ROLLING_WINDOW, min_periods=1).mean()
    )
    team_games["rolling_goals_against"] = (
        team_games["goals_against"].rolling(ROLLING_WINDOW, min_periods=1).mean()
    )
    team_games["rolling_goal_differential"] = (
        team_games["goal_differential"].rolling(ROLLING_WINDOW, min_periods=1).mean()
    )

    return TrendsResult(
        game_type=game_type.value,
        games=_dataframe_to_trend_games(team_games),
    )
