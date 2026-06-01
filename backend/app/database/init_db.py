from app.database.connection import get_connection

SCHEMA_VERSION = 2


def _get_current_version(connection) -> int:
    row = connection.execute("SELECT MAX(version) FROM schema_version").fetchone()
    return int(row[0]) if row[0] is not None else 0


def _migrate_to_v2(connection) -> None:
    connection.execute("DROP TABLE IF EXISTS games")
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS schedule_snapshots (
            team_abbr TEXT NOT NULL,
            season TEXT NOT NULL,
            response_json TEXT NOT NULL,
            fetched_at TEXT NOT NULL,
            PRIMARY KEY (team_abbr, season)
        );

        CREATE TABLE IF NOT EXISTS games (
            game_id INTEGER NOT NULL PRIMARY KEY,
            season INTEGER NOT NULL,
            game_type INTEGER,
            game_date TEXT,
            start_time_utc TEXT,
            game_state TEXT,
            venue TEXT,
            home_team_abbr TEXT,
            away_team_abbr TEXT,
            home_score INTEGER,
            away_score INTEGER,
            raw_game_json TEXT,
            updated_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_games_season_date
            ON games (season, game_date);
        """
    )


def init_db() -> None:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER NOT NULL PRIMARY KEY,
                applied_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            """
        )

        current_version = _get_current_version(connection)
        if current_version < SCHEMA_VERSION:
            _migrate_to_v2(connection)
            connection.execute(
                """
                INSERT OR REPLACE INTO schema_version (version)
                VALUES (?)
                """,
                (SCHEMA_VERSION,),
            )

        connection.commit()
