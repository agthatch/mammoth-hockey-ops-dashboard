from unittest.mock import patch

import pytest

from app.models.seasons import DEFAULT_SEASON_ID, parse_season_query
from tests.fixtures.nhl_schedule import (
    SAMPLE_GAME_OTHER_SEASON,
    SAMPLE_SCHEDULE_RESPONSE,
    TEAM_SUMMARY_SCHEDULE_RESPONSE,
)


def test_parse_season_query_accepts_supported_season():
    assert parse_season_query("20252026") == "20252026"


def test_parse_season_query_rejects_invalid_format():
    with pytest.raises(ValueError, match="Invalid season"):
        parse_season_query("abc")

    with pytest.raises(ValueError, match="Invalid season"):
        parse_season_query("202526")


def test_parse_season_query_rejects_unsupported_season():
    with pytest.raises(ValueError, match="Unsupported season"):
        parse_season_query("20232024")


def test_get_seasons_returns_supported_list(client):
    response = client.get("/api/seasons")

    assert response.status_code == 200
    payload = response.json()
    assert payload["default"] == DEFAULT_SEASON_ID
    assert payload["default"] == "20252026"
    assert len(payload["seasons"]) == 3
    assert payload["seasons"][0] == {"id": "20242025", "label": "2024-2025"}
    assert payload["seasons"][1] == {"id": "20252026", "label": "2025-2026"}
    assert payload["seasons"][2] == {"id": "20262027", "label": "2026-2027"}


def test_get_team_summary_rejects_invalid_season(client):
    response = client.get("/api/team-summary?season=invalid")

    assert response.status_code == 422


def test_get_team_summary_rejects_unsupported_season(client):
    response = client.get("/api/team-summary?season=20232024")

    assert response.status_code == 422
    assert "Unsupported season" in response.json()["detail"]


def test_get_team_summary_defaults_to_current_season(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = TEAM_SUMMARY_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20252026")

    response = client.get("/api/team-summary")

    assert response.status_code == 200
    assert response.json()["season"] == "20252026"
    assert response.json()["games_played"] == 4


def test_get_team_summary_empty_supported_season(client):
    response = client.get("/api/team-summary?season=20242025")

    assert response.status_code == 200
    payload = response.json()
    assert payload["season"] == "20242025"
    assert payload["games_played"] == 0


def test_get_team_summary_filters_by_season(client):
    mixed_response = {
        "clubTimezone": "America/Denver",
        "clubUTCOffset": "-06:00",
        "games": TEAM_SUMMARY_SCHEDULE_RESPONSE["games"] + [SAMPLE_GAME_OTHER_SEASON],
    }

    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = mixed_response
        client.post("/api/ingest/schedule?season=20252026")

    response_2526 = client.get("/api/team-summary?season=20252026")
    response_2627 = client.get("/api/team-summary?season=20262027")

    assert response_2526.json()["games_played"] == 4
    assert response_2627.json()["games_played"] == 0


def test_get_trends_includes_season_and_filters_by_season(client):
    mixed_response = {
        "clubTimezone": "America/Denver",
        "clubUTCOffset": "-06:00",
        "games": TEAM_SUMMARY_SCHEDULE_RESPONSE["games"] + [SAMPLE_GAME_OTHER_SEASON],
    }

    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = mixed_response
        client.post("/api/ingest/schedule?season=20252026")

    response_2526 = client.get("/api/trends?season=20252026&limit=20")
    response_2627 = client.get("/api/trends?season=20262027&limit=20")

    assert response_2526.status_code == 200
    assert response_2526.json()["season"] == "20252026"
    assert len(response_2526.json()["games"]) == 4

    assert response_2627.status_code == 200
    assert response_2627.json()["season"] == "20262027"
    assert response_2627.json()["games"] == []


def test_get_trends_rejects_unsupported_season(client):
    response = client.get("/api/trends?season=20232024")

    assert response.status_code == 422


def test_get_games_rejects_unsupported_season(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = SAMPLE_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20252026")

    response = client.get("/api/games?season=20232024")

    assert response.status_code == 422
