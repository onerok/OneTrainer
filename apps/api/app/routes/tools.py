from fastapi import APIRouter

from ..schemas import ToolsConfigResponse
from ..services.tools_service import get_tools_config as get_tools_config_service

router = APIRouter()


@router.get("/api/v1/tools-config", response_model=ToolsConfigResponse)
def get_tools_config() -> ToolsConfigResponse:
    return get_tools_config_service()
