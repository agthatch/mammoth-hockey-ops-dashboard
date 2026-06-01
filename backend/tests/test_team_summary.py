from unittest.mock import patch

import pytest

from app.analytics.team_summary import compute_team_summary
from app.models.game_types import (
    DEFAULT_GAME_TYPE,
    GameTypeCode,
    parse_game_type_query,
    to_nhl_game_type,
)
from tests.fixtures.nhl_schedule import TEAM_SUMMARY_SCHEDULE_RESPONSE


def test_parse_game_type_query_defaults_to_regular_season():
    assert parse_game_type_query(None) == DEFAULT_GAME_TYPE
    assert parse_game_type_query("") == GameTypeCode.R
    assert parse_game_type_query("r") == GameTypeCode.R


def test_parse_game_type_query_rejects_invalid_value():
    with pytest.raises(ValueError, match="Invalid game_type"):
        parse_game_type_query("foo")


def test_to_nhl_game_type_maps_codes():
    assert to_nhl_game_type(GameTypeCode.PR) == 1
    assert to_nhl_game_type(GameTypeCode.R) == 2
    assert to_nhl_game_type(GameTypeCode.P) == 3


def test_compute_team_summary_returns_zeros_for_empty_database(client):
    result = compute_team_summary(20252026, "UTA", GameTypeCode.R)

    assert result.games_played == 0
    assert result.wins == 0
    assert result.losses == 0
    assert result.ot_losses == 0
    assert result.points == 0
    assert result.goals_for == 0
    assert result.goals_against == 0
    assert result.goal_differential == 0


def test_compute_team_summary_regular_season_metrics(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = TEAM_SUMMARY_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20252026")

    result = compute_team_summary(20252026, "UTA", GameTypeCode.R)

    assert result.games_played == 4
    assert result.wins == 1
    assert result.losses == 1
    assert result.ot_losses == 2
    assert result.points == 4
    assert result.goals_for == 9
    assert result.goals_against == 10
    assert result.goal_differential == -1


def test_compute_team_summary_preseason_metrics(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = TEAM_SUMMARY_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20252026")

    result = compute_team_summary(20252026, "UTA", GameTypeCode.PR)

    assert result.games_played == 2
    assert result.wins == 0
    assert result.losses == 2
    assert result.ot_losses == 0
    assert result.points == 0
    assert result.goals_for == 4
    assert result.goals_against == 9


def test_get_team_summary_returns_regular_season_by_default(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = TEAM_SUMMARY_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20252026")

    response = client.get("/api/team-summary?season=20252026")

    assert response.status_code == 200
    payload = response.json()
    assert payload["season"] == "20252026"
    assert payload["game_type"] == "R"
    assert payload["games_played"] == 4
    assert payload["wins"] == 1
    assert payload["losses"] == 1
    assert payload["ot_losses"] == 2
    assert payload["points"] == 4
    assert payload["goals_for"] == 9
    assert payload["goals_against"] == 10
    assert payload["goal_differential"] == -1


def test_get_team_summary_filters_preseason(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = TEAM_SUMMARY_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20252026")

    response = client.get("/api/team-summary?season=20252026&game_type=PR")

    assert response.status_code == 200
    payload = response.json()
    assert payload["game_type"] == "PR"
    assert payload["games_played"] == 2
    assert payload["losses"] == 2


def test_get_team_summary_returns_zeros_when_no_games(client):
    response = client.get("/api/team-summary?season=20252026")

    assert response.status_code == 200
    payload = response.json()
    assert payload["games_played"] == 0
    assert payload["points"] == 0


def test_get_team_summary_rejects_invalid_game_type(client):
    response = client.get("/api/team-summary?game_type=foo")

    assert response.status_code == 422
