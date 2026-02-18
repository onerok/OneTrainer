from fastapi import APIRouter

from ..schemas import LoraConfigResponse, SaveLoraConfigRequest
from ..services.lora_service import get_lora_config as get_lora_config_service
from ..services.lora_service import save_lora_config as save_lora_config_service

router = APIRouter()


@router.get("/api/v1/lora-config", response_model=LoraConfigResponse)
def get_lora_config() -> LoraConfigResponse:
    return get_lora_config_service()


@router.post("/api/v1/lora-config", response_model=LoraConfigResponse)
def save_lora_config(body: SaveLoraConfigRequest) -> LoraConfigResponse:
    return save_lora_config_service(body.data)
