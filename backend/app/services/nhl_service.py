"""NHL API integration service.

Integration with https://api-web.nhle.com/v1 for Utah Mammoth data:
- /club-schedule-season/UTA/20262027
- /gamecenter/{gameId}/boxscore
- /gamecenter/{gameId}/play-by-play

Raw API responses should be stored in SQLite whenever practical.
"""

import httpx

NHL_API_BASE_URL = "https://api-web.nhle.com/v1"


class NHLServiceError(Exception):
    """Raised when the NHL API request fails."""


class NHLService:
    """NHL API data ingestion service."""

    def fetch_schedule(self, season: str, team_abbr: str = "UTA") -> dict:
        url = f"{NHL_API_BASE_URL}/club-schedule-season/{team_abbr}/{season}"

        try:
            response = httpx.get(url, timeout=30.0)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise NHLServiceError(
                f"NHL API returned {exc.response.status_code} for {url}"
            ) from exc
        except httpx.RequestError as exc:
            raise NHLServiceError(f"NHL API request failed: {exc}") from exc

        return response.json()

    def fetch_boxscore(self, game_id: str) -> None:
        """Fetch boxscore for a game. Not yet implemented."""
        raise NotImplementedError("NHL boxscore ingestion is not yet implemented.")

    def fetch_play_by_play(self, game_id: str) -> None:
        """Fetch play-by-play data for a game. Not yet implemented."""
        raise NotImplementedError("NHL play-by-play ingestion is not yet implemented.")
