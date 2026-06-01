from unittest.mock import patch

from tests.fixtures.nhl_schedule import (
    SAMPLE_GAME_OTHER_SEASON,
    SAMPLE_SCHEDULE_RESPONSE,
)


def test_get_games_returns_empty_list(client):
    response = client.get("/api/games?season=20252026")

    assert response.status_code == 200
    payload = response.json()
    assert payload["season"] == "20252026"
    assert payload["count"] == 0
    assert payload["games"] == []


def test_get_games_returns_ingested_schedule(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = SAMPLE_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20252026")

    response = client.get("/api/games?season=20252026")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 2
    assert [game["game_id"] for game in payload["games"]] == [2025010103, 2025010104]
    assert payload["games"][0]["home_team_abbr"] == "UTA"
    assert payload["games"][0]["away_team_abbr"] == "COL"
    assert payload["games"][0]["home_score"] == 3
    assert payload["games"][0]["away_score"] == 5
    assert payload["games"][1]["game_state"] == "FUT"


def test_get_games_filters_by_season(client):
    mixed_response = {
        "clubTimezone": "America/Denver",
        "clubUTCOffset": "-06:00",
        "games": SAMPLE_SCHEDULE_RESPONSE["games"] + [SAMPLE_GAME_OTHER_SEASON],
    }

    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = mixed_response
        client.post("/api/ingest/schedule?season=20252026")

    response = client.get("/api/games?season=20262027")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1
    assert payload["games"][0]["game_id"] == 2026010101
