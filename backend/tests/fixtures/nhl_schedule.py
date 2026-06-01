SAMPLE_GAME_1 = {
    "id": 2025010103,
    "season": 20252026,
    "gameType": 1,
    "gameDate": "2025-09-21",
    "venue": {"default": "Magness Arena"},
    "startTimeUTC": "2025-09-21T23:00:00Z",
    "gameState": "FINAL",
    "awayTeam": {"abbrev": "COL", "score": 5},
    "homeTeam": {"abbrev": "UTA", "score": 3},
}

SAMPLE_GAME_2 = {
    "id": 2025010104,
    "season": 20252026,
    "gameType": 1,
    "gameDate": "2025-09-22",
    "venue": {"default": "Delta Center"},
    "startTimeUTC": "2025-09-22T23:00:00Z",
    "gameState": "FUT",
    "awayTeam": {"abbrev": "VGK", "score": None},
    "homeTeam": {"abbrev": "UTA", "score": None},
}

SAMPLE_GAME_OTHER_SEASON = {
    "id": 2026010101,
    "season": 20262027,
    "gameType": 2,
    "gameDate": "2026-10-01",
    "venue": {"default": "Delta Center"},
    "startTimeUTC": "2026-10-01T23:00:00Z",
    "gameState": "FUT",
    "awayTeam": {"abbrev": "VGK"},
    "homeTeam": {"abbrev": "UTA"},
}

SAMPLE_SCHEDULE_RESPONSE = {
    "clubTimezone": "America/Denver",
    "clubUTCOffset": "-06:00",
    "games": [SAMPLE_GAME_1, SAMPLE_GAME_2],
}

EMPTY_SCHEDULE_RESPONSE = {
    "clubTimezone": "America/Denver",
    "clubUTCOffset": "-06:00",
    "games": [],
}

REGULAR_SEASON_WIN = {
    "id": 2025020001,
    "season": 20252026,
    "gameType": 2,
    "gameDate": "2025-10-10",
    "venue": {"default": "Delta Center"},
    "startTimeUTC": "2025-10-10T23:00:00Z",
    "gameState": "FINAL",
    "gameOutcome": {"lastPeriodType": "REG"},
    "awayTeam": {"abbrev": "VGK", "score": 2},
    "homeTeam": {"abbrev": "UTA", "score": 4},
}

REGULAR_SEASON_REG_LOSS = {
    "id": 2025020002,
    "season": 20252026,
    "gameType": 2,
    "gameDate": "2025-10-12",
    "venue": {"default": "Delta Center"},
    "startTimeUTC": "2025-10-12T23:00:00Z",
    "gameState": "FINAL",
    "gameOutcome": {"lastPeriodType": "REG"},
    "awayTeam": {"abbrev": "UTA", "score": 2},
    "homeTeam": {"abbrev": "COL", "score": 3},
}

REGULAR_SEASON_OT_LOSS = {
    "id": 2025020003,
    "season": 20252026,
    "gameType": 2,
    "gameDate": "2025-10-14",
    "venue": {"default": "Delta Center"},
    "startTimeUTC": "2025-10-14T23:00:00Z",
    "gameState": "OFF",
    "gameOutcome": {"lastPeriodType": "OT"},
    "awayTeam": {"abbrev": "DAL", "score": 3},
    "homeTeam": {"abbrev": "UTA", "score": 2},
}

REGULAR_SEASON_SO_LOSS = {
    "id": 2025020004,
    "season": 20252026,
    "gameType": 2,
    "gameDate": "2025-10-16",
    "venue": {"default": "Delta Center"},
    "startTimeUTC": "2025-10-16T23:00:00Z",
    "gameState": "FINAL",
    "gameOutcome": {"lastPeriodType": "SO"},
    "awayTeam": {"abbrev": "UTA", "score": 1},
    "homeTeam": {"abbrev": "SEA", "score": 2},
}

REGULAR_SEASON_FUTURE = {
    "id": 2025020005,
    "season": 20252026,
    "gameType": 2,
    "gameDate": "2026-04-10",
    "venue": {"default": "Delta Center"},
    "startTimeUTC": "2026-04-10T23:00:00Z",
    "gameState": "FUT",
    "awayTeam": {"abbrev": "VGK"},
    "homeTeam": {"abbrev": "UTA"},
}

PRESEASON_FINAL_LOSS = {
    "id": 2025010201,
    "season": 20252026,
    "gameType": 1,
    "gameDate": "2025-09-20",
    "venue": {"default": "Magness Arena"},
    "startTimeUTC": "2025-09-20T23:00:00Z",
    "gameState": "FINAL",
    "gameOutcome": {"lastPeriodType": "REG"},
    "awayTeam": {"abbrev": "COL", "score": 4},
    "homeTeam": {"abbrev": "UTA", "score": 1},
}

TEAM_SUMMARY_SCHEDULE_RESPONSE = {
    "clubTimezone": "America/Denver",
    "clubUTCOffset": "-06:00",
    "games": [
        REGULAR_SEASON_WIN,
        REGULAR_SEASON_REG_LOSS,
        REGULAR_SEASON_OT_LOSS,
        REGULAR_SEASON_SO_LOSS,
        REGULAR_SEASON_FUTURE,
        PRESEASON_FINAL_LOSS,
        SAMPLE_GAME_1,
        SAMPLE_GAME_2,
    ],
}
