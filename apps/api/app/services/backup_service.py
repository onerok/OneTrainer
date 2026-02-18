from modules.util.enum.TimeUnit import TimeUnit  # noqa: E402

from ..core.store import store
from ..mappers.backup import apply_backup_settings, to_backup_settings
from ..schemas import BackupConfigResponse, BackupMeta, BackupSettings


def get_backup_config() -> BackupConfigResponse:
    config = store.load()
    return BackupConfigResponse(
        data=to_backup_settings(config),
        meta=BackupMeta(
            backup_after_units=[unit.value for unit in TimeUnit],
            save_every_units=[unit.value for unit in TimeUnit],
        ),
    )


def save_backup_config(settings: BackupSettings) -> BackupConfigResponse:
    config = store.load()
    config = apply_backup_settings(config, settings)
    store.save(config)
    return BackupConfigResponse(
        data=to_backup_settings(config),
        meta=BackupMeta(
            backup_after_units=[unit.value for unit in TimeUnit],
            save_every_units=[unit.value for unit in TimeUnit],
        ),
    )
