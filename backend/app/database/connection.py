import sqlite3

from app.config.settings import settings


def get_connection() -> sqlite3.Connection:
    db_path = settings.resolved_database_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection
