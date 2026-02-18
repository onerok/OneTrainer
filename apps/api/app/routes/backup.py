from fastapi import APIRouter

from ..schemas import BackupConfigResponse, SaveBackupConfigRequest
from ..services.backup_service import get_backup_config as get_backup_config_service
from ..services.backup_service import save_backup_config as save_backup_config_service

router = APIRouter()


@router.get("/api/v1/backup-config", response_model=BackupConfigResponse)
def get_backup_config() -> BackupConfigResponse:
    return get_backup_config_service()


@router.post("/api/v1/backup-config", response_model=BackupConfigResponse)
def save_backup_config(body: SaveBackupConfigRequest) -> BackupConfigResponse:
    return save_backup_config_service(body.data)
