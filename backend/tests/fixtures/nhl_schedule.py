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
