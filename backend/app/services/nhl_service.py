"""NHL API integration service.

Future integration with https://api-web.nhle.com/v1 for Utah Mammoth data:
- /club-schedule-season/UTA/20262027
- /gamecenter/{gameId}/boxscore
- /gamecenter/{gameId}/play-by-play

Raw API responses should be stored in SQLite whenever practical.
"""

NHL_API_BASE_URL = "https://api-web.nhle.com/v1"


class NHLService:
    """Placeholder for NHL API data ingestion."""

    def fetch_schedule(self, season: str) -> None:
        """Fetch team schedule for the given season. Not yet implemented."""
        raise NotImplementedError("NHL schedule ingestion is not yet implemented.")

    def fetch_boxscore(self, game_id: str) -> None:
        """Fetch boxscore for a game. Not yet implemented."""
        raise NotImplementedError("NHL boxscore ingestion is not yet implemented.")

    def fetch_play_by_play(self, game_id: str) -> None:
        """Fetch play-by-play data for a game. Not yet implemented."""
        raise NotImplementedError("NHL play-by-play ingestion is not yet implemented.")
