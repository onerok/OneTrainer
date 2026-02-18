from fastapi import APIRouter

from ..schemas import ConceptsConfigResponse, SaveConceptsConfigRequest
from ..services.concepts_service import get_concepts_config as get_concepts_config_service
from ..services.concepts_service import save_concepts_config as save_concepts_config_service

router = APIRouter()


@router.get("/api/v1/concepts-config", response_model=ConceptsConfigResponse)
def get_concepts_config() -> ConceptsConfigResponse:
    return get_concepts_config_service()


@router.post("/api/v1/concepts-config", response_model=ConceptsConfigResponse)
def save_concepts_config(body: SaveConceptsConfigRequest) -> ConceptsConfigResponse:
    return save_concepts_config_service(body.data)
