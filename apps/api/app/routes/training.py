from fastapi import APIRouter

from ..schemas import SaveTrainingConfigRequest, TrainingConfigResponse
from ..services.training_service import get_training_config as get_training_config_service
from ..services.training_service import save_training_config as save_training_config_service

router = APIRouter()


@router.get("/api/v1/training-config", response_model=TrainingConfigResponse)
def get_training_config() -> TrainingConfigResponse:
    return get_training_config_service()


@router.post("/api/v1/training-config", response_model=TrainingConfigResponse)
def save_training_config(body: SaveTrainingConfigRequest) -> TrainingConfigResponse:
    return save_training_config_service(body.data)
