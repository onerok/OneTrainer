from fastapi import APIRouter

from modules.util.enum.TimeUnit import TimeUnit  # noqa: E402

from ..core.store import store
from ..schemas import BackupConfigResponse, BackupMeta, BackupSettings, SaveBackupConfigRequest

router = APIRouter()


def _to_backup_settings(config) -> BackupSettings:
    return BackupSettings(
        backup_after=config.backup_after,
        backup_after_unit=config.backup_after_unit.value,
        rolling_backup=config.rolling_backup,
        rolling_backup_count=config.rolling_backup_count,
        backup_before_save=config.backup_before_save,
        save_every=config.save_every,
        save_every_unit=config.save_every_unit.value,
        save_skip_first=config.save_skip_first,
        save_filename_prefix=config.save_filename_prefix,
    )


def _apply_backup_settings(config, settings: BackupSettings):
    payload = settings.model_dump()
    config.backup_after = payload["backup_after"]
    config.backup_after_unit = TimeUnit[payload["backup_after_unit"]]
    config.rolling_backup = payload["rolling_backup"]
    config.rolling_backup_count = payload["rolling_backup_count"]
    config.backup_before_save = payload["backup_before_save"]
    config.save_every = payload["save_every"]
    config.save_every_unit = TimeUnit[payload["save_every_unit"]]
    config.save_skip_first = payload["save_skip_first"]
    config.save_filename_prefix = payload["save_filename_prefix"]
    return config


@router.get("/api/v1/backup-config", response_model=BackupConfigResponse)
def get_backup_config() -> BackupConfigResponse:
    config = store.load()
    return BackupConfigResponse(
        data=_to_backup_settings(config),
        meta=BackupMeta(
            backup_after_units=[unit.value for unit in TimeUnit],
            save_every_units=[unit.value for unit in TimeUnit],
        ),
    )


@router.post("/api/v1/backup-config", response_model=BackupConfigResponse)
def save_backup_config(body: SaveBackupConfigRequest) -> BackupConfigResponse:
    config = store.load()
    config = _apply_backup_settings(config, body.data)
    store.save(config)
    return BackupConfigResponse(
        data=_to_backup_settings(config),
        meta=BackupMeta(
            backup_after_units=[unit.value for unit in TimeUnit],
            save_every_units=[unit.value for unit in TimeUnit],
        ),
    )
