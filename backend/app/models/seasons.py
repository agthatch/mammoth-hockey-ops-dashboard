"""Supported NHL seasons for dashboard analytics."""

from dataclasses import dataclass

from app.config.settings import settings


@dataclass(frozen=True)
class SeasonOption:
    id: str
    label: str


SUPPORTED_SEASONS: tuple[SeasonOption, ...] = (
    SeasonOption(id="20242025", label="2024-2025"),
    SeasonOption(id="20252026", label="2025-2026"),
    SeasonOption(id="20262027", label="2026-2027"),
)

DEFAULT_SEASON_ID = settings.nhl_default_season

SUPPORTED_SEASON_IDS = frozenset(season.id for season in SUPPORTED_SEASONS)


def parse_season_query(season: str) -> str:
    """Validate season query param; return canonical season id string."""
    if not season or not season.isdigit() or len(season) != 8:
        raise ValueError(f"Invalid season: {season!r}. Expected an 8-digit NHL season id.")

    if season not in SUPPORTED_SEASON_IDS:
        raise ValueError(f"Unsupported season: {season}")

    return season


def season_to_int(season: str) -> int:
    return int(parse_season_query(season))
