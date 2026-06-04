from fastapi import APIRouter

from app.models.schemas import SeasonListResponse, SeasonOptionResponse
from app.models.seasons import DEFAULT_SEASON_ID, SUPPORTED_SEASONS

router = APIRouter(tags=["seasons"])


@router.get("/seasons", response_model=SeasonListResponse)
def list_seasons() -> SeasonListResponse:
    return SeasonListResponse(
        default=DEFAULT_SEASON_ID,
        seasons=[
            SeasonOptionResponse(id=season.id, label=season.label)
            for season in SUPPORTED_SEASONS
        ],
    )
