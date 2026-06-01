"""NHL game type codes shared by API and analytics layers."""

from enum import StrEnum


class GameTypeCode(StrEnum):
    PR = "PR"  # Preseason
    R = "R"    # Regular season
    P = "P"    # Playoffs


DEFAULT_GAME_TYPE = GameTypeCode.R

_NHL_GAME_TYPE_BY_CODE: dict[GameTypeCode, int] = {
    GameTypeCode.PR: 1,
    GameTypeCode.R: 2,
    GameTypeCode.P: 3,
}

_CODE_BY_NHL_GAME_TYPE: dict[int, GameTypeCode] = {
    value: key for key, value in _NHL_GAME_TYPE_BY_CODE.items()
}

_LABELS: dict[GameTypeCode, str] = {
    GameTypeCode.PR: "Preseason",
    GameTypeCode.R: "Regular Season",
    GameTypeCode.P: "Playoffs",
}


def to_nhl_game_type(code: GameTypeCode) -> int:
    return _NHL_GAME_TYPE_BY_CODE[code]


def from_nhl_game_type(value: int) -> GameTypeCode | None:
    return _CODE_BY_NHL_GAME_TYPE.get(value)


def parse_game_type_query(value: str | None) -> GameTypeCode:
    if value is None or value.strip() == "":
        return DEFAULT_GAME_TYPE

    normalized = value.strip().upper()
    try:
        return GameTypeCode(normalized)
    except ValueError as exc:
        raise ValueError(
            f"Invalid game_type '{value}'. Expected one of: PR, R, P."
        ) from exc


def game_type_label(code: GameTypeCode) -> str:
    return _LABELS[code]
