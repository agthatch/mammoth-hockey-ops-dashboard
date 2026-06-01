from unittest.mock import patch

from app.services.nhl_service import NHLServiceError
from tests.fixtures.nhl_schedule import (
    EMPTY_SCHEDULE_RESPONSE,
    SAMPLE_SCHEDULE_RESPONSE,
)


def test_ingest_schedule_stores_games(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = SAMPLE_SCHEDULE_RESPONSE
        response = client.post("/api/ingest/schedule?season=20252026")

    assert response.status_code == 200
    payload = response.json()
    assert payload["team_abbr"] == "UTA"
    assert payload["season"] == "20252026"
    assert payload["games_ingested"] == 2
    assert payload["fetched_at"]


def test_ingest_schedule_handles_empty_games(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.return_value = EMPTY_SCHEDULE_RESPONSE
        response = client.post("/api/ingest/schedule?season=20262027")

    assert response.status_code == 200
    payload = response.json()
    assert payload["games_ingested"] == 0
    assert payload["season"] == "20262027"


def test_ingest_schedule_returns_502_on_nhl_error(client):
    with patch("app.api.ingest.NHLService") as mock_service:
        mock_service.return_value.fetch_schedule.side_effect = NHLServiceError(
            "NHL API returned 503"
        )
        response = client.post("/api/ingest/schedule")

    assert response.status_code == 502
    assert "503" in response.json()["detail"]
