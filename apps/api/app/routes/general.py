from fastapi import APIRouter

from ..schemas import GeneralConfigResponse, SaveGeneralConfigRequest
from ..services.general_service import get_general_config as get_general_config_service
from ..services.general_service import save_general_config as save_general_config_service

router = APIRouter()


@router.get("/api/v1/general-config", response_model=GeneralConfigResponse)
def get_general_config() -> GeneralConfigResponse:
    return get_general_config_service()


@router.post("/api/v1/general-config", response_model=GeneralConfigResponse)
def save_general_config(body: SaveGeneralConfigRequest) -> GeneralConfigResponse:
    return save_general_config_service(body.data)


@router.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
