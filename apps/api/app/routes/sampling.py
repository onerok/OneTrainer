from fastapi import APIRouter

from ..schemas import SamplingConfigResponse, SaveSamplingConfigRequest
from ..services.sampling_service import get_sampling_config as get_sampling_config_service
from ..services.sampling_service import save_sampling_config as save_sampling_config_service

router = APIRouter()


@router.get("/api/v1/sampling-config", response_model=SamplingConfigResponse)
def get_sampling_config() -> SamplingConfigResponse:
    return get_sampling_config_service()


@router.post("/api/v1/sampling-config", response_model=SamplingConfigResponse)
def save_sampling_config(body: SaveSamplingConfigRequest) -> SamplingConfigResponse:
    return save_sampling_config_service(body.data)
