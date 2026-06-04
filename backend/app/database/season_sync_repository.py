from app.database.connection import get_connection


def get_season_sync(team_abbr: str, season: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT last_sync_at, game_count
            FROM season_sync_metadata
            WHERE team_abbr = ? AND season = ?
            """,
            (team_abbr, season),
        ).fetchone()

    if row is None:
        return None

    return {"last_sync_at": row["last_sync_at"], "game_count": row["game_count"]}


def upsert_season_sync(
    team_abbr: str,
    season: str,
    last_sync_at: str,
    game_count: int,
) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO season_sync_metadata (team_abbr, season, last_sync_at, game_count)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (team_abbr, season) DO UPDATE SET
                last_sync_at = excluded.last_sync_at,
                game_count = excluded.game_count
            """,
            (team_abbr, season, last_sync_at, game_count),
        )
        connection.commit()
