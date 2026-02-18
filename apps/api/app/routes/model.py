from fastapi import APIRouter

from ..schemas import ModelConfigResponse, SaveModelConfigRequest
from ..services.model_service import get_model_config as get_model_config_service
from ..services.model_service import save_model_config as save_model_config_service

router = APIRouter()


@router.get("/api/v1/model-config", response_model=ModelConfigResponse)
def get_model_config() -> ModelConfigResponse:
    return get_model_config_service()


@router.post("/api/v1/model-config", response_model=ModelConfigResponse)
def save_model_config(body: SaveModelConfigRequest) -> ModelConfigResponse:
    return save_model_config_service(body.data)
