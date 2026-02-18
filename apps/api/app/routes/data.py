from fastapi import APIRouter

from ..schemas import DataConfigResponse, SaveDataConfigRequest
from ..services.data_service import get_data_config as get_data_config_service
from ..services.data_service import save_data_config as save_data_config_service

router = APIRouter()


@router.get("/api/v1/data-config", response_model=DataConfigResponse)
def get_data_config() -> DataConfigResponse:
    return get_data_config_service()


@router.post("/api/v1/data-config", response_model=DataConfigResponse)
def save_data_config(body: SaveDataConfigRequest) -> DataConfigResponse:
    return save_data_config_service(body.data)
