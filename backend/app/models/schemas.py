"""Pydantic response models for API endpoints."""

from pydantic import BaseModel


class IngestScheduleResponse(BaseModel):
    team_abbr: str
    season: str
    games_ingested: int
    fetched_at: str


class GameResponse(BaseModel):
    game_id: int
    season: int
    game_type: int | None
    game_date: str | None
    start_time_utc: str | None
    game_state: str | None
    venue: str | None
    home_team_abbr: str | None
    away_team_abbr: str | None
    home_score: int | None
    away_score: int | None


class GamesListResponse(BaseModel):
    season: str
    count: int
    games: list[GameResponse]


class TeamSummaryResponse(BaseModel):
    season: str
    game_type: str
    games_played: int
    wins: int
    losses: int
    ot_losses: int
    points: int
    goals_for: int
    goals_against: int
    goal_differential: int


class TrendGameResponse(BaseModel):
    game_id: int
    game_date: str
    goals_for: int
    goals_against: int
    goal_differential: int
    rolling_goals_for: float
    rolling_goals_against: float
    rolling_goal_differential: float


class TrendsResponse(BaseModel):
    game_type: str
    games: list[TrendGameResponse]
