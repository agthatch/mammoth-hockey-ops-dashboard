import json
from datetime import UTC, datetime

from app.database.connection import get_connection

GAME_COLUMNS = (
    "game_id",
    "season",
    "game_type",
    "game_date",
    "start_time_utc",
    "game_state",
    "venue",
    "home_team_abbr",
    "away_team_abbr",
    "home_score",
    "away_score",
    "raw_game_json",
    "updated_at",
)


def _parse_game(game: dict) -> dict:
    venue = game.get("venue") or {}
    home = game.get("homeTeam") or {}
    away = game.get("awayTeam") or {}

    return {
        "game_id": game["id"],
        "season": game["season"],
        "game_type": game.get("gameType"),
        "game_date": game.get("gameDate"),
        "start_time_utc": game.get("startTimeUTC"),
        "game_state": game.get("gameState"),
        "venue": venue.get("default"),
        "home_team_abbr": home.get("abbrev"),
        "away_team_abbr": away.get("abbrev"),
        "home_score": home.get("score"),
        "away_score": away.get("score"),
        "raw_game_json": json.dumps(game),
    }


def save_schedule_snapshot(team_abbr: str, season: str, response_dict: dict) -> str:
    fetched_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO schedule_snapshots (team_abbr, season, response_json, fetched_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (team_abbr, season) DO UPDATE SET
                response_json = excluded.response_json,
                fetched_at = excluded.fetched_at
            """,
            (team_abbr, season, json.dumps(response_dict), fetched_at),
        )
        connection.commit()

    return fetched_at


def upsert_games(games_list: list[dict]) -> int:
    if not games_list:
        return 0

    updated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    placeholders = ", ".join("?" for _ in GAME_COLUMNS)
    update_assignments = ", ".join(
        f"{column} = excluded.{column}" for column in GAME_COLUMNS if column != "game_id"
    )

    with get_connection() as connection:
        for game in games_list:
            parsed = _parse_game(game)
            parsed["updated_at"] = updated_at
            values = tuple(parsed[column] for column in GAME_COLUMNS)
            connection.execute(
                f"""
                INSERT INTO games ({", ".join(GAME_COLUMNS)})
                VALUES ({placeholders})
                ON CONFLICT (game_id) DO UPDATE SET
                    {update_assignments}
                """,
                values,
            )
        connection.commit()

    return len(games_list)


def list_games(season: int | None = None) -> list[dict]:
    select_columns = ", ".join(GAME_COLUMNS)

    with get_connection() as connection:
        if season is not None:
            rows = connection.execute(
                f"""
                SELECT {select_columns}
                FROM games
                WHERE season = ?
                ORDER BY game_date, start_time_utc
                """,
                (season,),
            ).fetchall()
        else:
            rows = connection.execute(
                f"""
                SELECT {select_columns}
                FROM games
                ORDER BY game_date, start_time_utc
                """
            ).fetchall()

    return [dict(row) for row in rows]
