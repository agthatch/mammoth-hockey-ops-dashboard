from app.database.connection import get_connection

SCHEMA_VERSION = 1


def init_db() -> None:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER NOT NULL PRIMARY KEY,
                applied_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            -- Placeholder for future NHL game data ingestion.
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                game_id TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            """
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO schema_version (version)
            VALUES (?)
            """,
            (SCHEMA_VERSION,),
        )
        connection.commit()
