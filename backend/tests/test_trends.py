from unittest.mock import patch

import pytest

from app.analytics.trends import compute_trends
from app.models.game_types import GameTypeCode
from tests.fixtures.nhl_schedule import TEAM_SUMMARY_SCHEDULE_RESPONSE


def _ingest_team_summary_fixture(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = TEAM_SUMMARY_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20252026")


def test_compute_trends_empty_database(client):
    result = compute_trends(20252026, "UTA", GameTypeCode.R)

    assert result.game_type == "R"
    assert result.games == []


def test_compute_trends_regular_season_filtering(client):
    _ingest_team_summary_fixture(client)

    result = compute_trends(20252026, "UTA", GameTypeCode.R)

    assert result.game_type == "R"
    assert len(result.games) == 4
    assert all(game.game_date for game in result.games)
    game_ids = [game.game_id for game in result.games]
    assert game_ids == [2025020001, 2025020002, 2025020003, 2025020004]


def test_compute_trends_preseason_filtering(client):
    _ingest_team_summary_fixture(client)

    result = compute_trends(20252026, "UTA", GameTypeCode.PR)

    assert result.game_type == "PR"
    assert len(result.games) == 2
    game_ids = [game.game_id for game in result.games]
    assert game_ids == [2025010201, 2025010103]


def test_compute_trends_limit(client):
    _ingest_team_summary_fixture(client)

    result = compute_trends(20252026, "UTA", GameTypeCode.R, limit=2)

    assert len(result.games) == 2
    game_ids = [game.game_id for game in result.games]
    assert game_ids == [2025020003, 2025020004]


def test_compute_trends_goal_differential(client):
    _ingest_team_summary_fixture(client)

    result = compute_trends(20252026, "UTA", GameTypeCode.R)

    first_game = result.games[0]
    assert first_game.game_id == 2025020001
    assert first_game.game_date == "2025-10-10"
    assert first_game.goals_for == 4
    assert first_game.goals_against == 2
    assert first_game.goal_differential == 2


def test_compute_trends_rolling_averages(client):
    _ingest_team_summary_fixture(client)

    result = compute_trends(20252026, "UTA", GameTypeCode.R)

    first_game = result.games[0]
    second_game = result.games[1]

    assert first_game.rolling_goals_for == pytest.approx(4.0)
    assert first_game.rolling_goals_against == pytest.approx(2.0)
    assert first_game.rolling_goal_differential == pytest.approx(2.0)

    assert second_game.rolling_goals_for == pytest.approx(3.0)
    assert second_game.rolling_goals_against == pytest.approx(2.5)
    assert second_game.rolling_goal_differential == pytest.approx(0.5)


def test_get_trends_returns_valid_payload(client):
    _ingest_team_summary_fixture(client)

    response = client.get("/api/trends?game_type=R&limit=20")

    assert response.status_code == 200
    payload = response.json()
    assert payload["season"] == "20252026"
    assert payload["game_type"] == "R"
    assert len(payload["games"]) == 4
    first_game = payload["games"][0]
    assert first_game["game_id"] == 2025020001
    assert first_game["game_date"] == "2025-10-10"
    assert first_game["goals_for"] == 4
    assert first_game["goals_against"] == 2
    assert first_game["goal_differential"] == 2
    assert first_game["rolling_goals_for"] == pytest.approx(4.0)


def test_get_trends_rejects_invalid_game_type(client):
    response = client.get("/api/trends?game_type=foo")

    assert response.status_code == 422


def test_get_trends_rejects_invalid_limit(client):
    response = client.get("/api/trends?limit=0")

    assert response.status_code == 422
