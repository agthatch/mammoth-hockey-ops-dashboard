"""Team summary analytics computed from stored game data."""

from dataclasses import dataclass
import json

import pandas as pd

from app.database.connection import get_connection
from app.models.game_types import GameTypeCode, to_nhl_game_type

COMPLETED_GAME_STATES = frozenset({"FINAL", "OFF"})
OT_LOSS_PERIOD_TYPES = frozenset({"OT", "SO"})

_GAMES_QUERY = """
    SELECT
        game_id,
        game_type,
        game_state,
        home_team_abbr,
        away_team_abbr,
        home_score,
        away_score,
        raw_game_json
    FROM games
    WHERE season = ?
      AND game_type = ?
"""


@dataclass(frozen=True)
class TeamSummaryResult:
    games_played: int
    wins: int
    losses: int
    ot_losses: int
    points: int
    goals_for: int
    goals_against: int
    goal_differential: int


def load_games_dataframe(season: int, game_type: int) -> pd.DataFrame:
    with get_connection() as connection:
        return pd.read_sql_query(
            _GAMES_QUERY,
            connection,
            params=(season, game_type),
        )


def _extract_last_period_type(raw_game_json: str | None) -> str | None:
    if not raw_game_json:
        return None

    try:
        payload = json.loads(raw_game_json)
    except json.JSONDecodeError:
        return None

    game_outcome = payload.get("gameOutcome") or {}
    return game_outcome.get("lastPeriodType")


def _prepare_team_games(games: pd.DataFrame, team_abbr: str) -> pd.DataFrame:
    if games.empty:
        return games.copy()

    team_games = games.loc[games["game_state"].isin(COMPLETED_GAME_STATES)].copy()
    if team_games.empty:
        return team_games

    team_games = team_games.dropna(subset=["home_score", "away_score"])
    if team_games.empty:
        return team_games

    team_abbr = team_abbr.upper()
    is_home = team_games["home_team_abbr"].str.upper() == team_abbr
    is_away = team_games["away_team_abbr"].str.upper() == team_abbr
    team_games = team_games.loc[is_home | is_away].copy()

    is_home = team_games["home_team_abbr"].str.upper() == team_abbr
    team_games["goals_for"] = team_games["home_score"].where(is_home, team_games["away_score"])
    team_games["goals_against"] = team_games["away_score"].where(
        is_home, team_games["home_score"]
    )
    team_games["is_win"] = team_games["goals_for"] > team_games["goals_against"]
    team_games["last_period_type"] = team_games["raw_game_json"].map(
        _extract_last_period_type
    )

    return team_games


def _empty_summary() -> TeamSummaryResult:
    return TeamSummaryResult(
        games_played=0,
        wins=0,
        losses=0,
        ot_losses=0,
        points=0,
        goals_for=0,
        goals_against=0,
        goal_differential=0,
    )


def compute_team_summary(
    season: int,
    team_abbr: str,
    game_type: GameTypeCode,
) -> TeamSummaryResult:
    games = load_games_dataframe(season, to_nhl_game_type(game_type))
    team_games = _prepare_team_games(games, team_abbr)

    if team_games.empty:
        return _empty_summary()

    wins = int(team_games["is_win"].sum())
    losses_mask = ~team_games["is_win"]
    ot_losses = int(
        (losses_mask & team_games["last_period_type"].isin(OT_LOSS_PERIOD_TYPES)).sum()
    )
    regulation_losses = int(losses_mask.sum()) - ot_losses

    goals_for = int(team_games["goals_for"].sum())
    goals_against = int(team_games["goals_against"].sum())

    return TeamSummaryResult(
        games_played=len(team_games),
        wins=wins,
        losses=regulation_losses,
        ot_losses=ot_losses,
        points=(wins * 2) + ot_losses,
        goals_for=goals_for,
        goals_against=goals_against,
        goal_differential=goals_for - goals_against,
    )
