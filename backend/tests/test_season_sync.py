from unittest.mock import patch

from app.services.nhl_service import NHLServiceError
from tests.fixtures.nhl_schedule import (
    EMPTY_SCHEDULE_RESPONSE,
    SAMPLE_SCHEDULE_RESPONSE,
)


def _get_status(client, season: str, team_abbr: str = "UTA"):
    return client.get(f"/api/season-status?season={season}&team_abbr={team_abbr}")


def test_ingest_creates_season_sync_metadata(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = SAMPLE_SCHEDULE_RESPONSE
        ingest = client.post("/api/ingest/schedule?season=20252026")

    assert ingest.status_code == 200
    status = _get_status(client, "20252026")
    assert status.status_code == 200
    payload = status.json()
    assert payload["season"] == "20252026"
    assert payload["team_abbr"] == "UTA"
    assert payload["last_sync_at"]
    assert payload["game_count"] == 2


def test_ingest_updates_season_sync_metadata(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = EMPTY_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20252026")
        empty_status = _get_status(client, "20252026").json()
        assert empty_status["game_count"] == 0
        assert empty_status["last_sync_at"]

        mock_service.return_value.fetch_schedule.return_value = SAMPLE_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20252026")
        updated_status = _get_status(client, "20252026").json()

    assert updated_status["game_count"] == 2
    assert updated_status["last_sync_at"]


def test_ingest_empty_schedule_updates_metadata(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = EMPTY_SCHEDULE_RESPONSE
        client.post("/api/ingest/schedule?season=20262027")

    status = _get_status(client, "20262027")
    payload = status.json()
    assert payload["game_count"] == 0
    assert payload["last_sync_at"]


def test_ingest_nhl_error_does_not_update_metadata(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.side_effect = NHLServiceError(
            "NHL API returned 503"
        )
        response = client.post("/api/ingest/schedule?season=20252026")

    assert response.status_code == 502
    status = _get_status(client, "20252026")
    payload = status.json()
    assert payload["last_sync_at"] is None
    assert payload["game_count"] == 0


def test_get_season_status_unsynchronized(client):
    response = _get_status(client, "20242025")

    assert response.status_code == 200
    payload = response.json()
    assert payload["season"] == "20242025"
    assert payload["team_abbr"] == "UTA"
    assert payload["last_sync_at"] is None
    assert payload["game_count"] == 0


def test_get_season_status_requires_season(client):
    response = client.get("/api/season-status")

    assert response.status_code == 422
