from modules.util.enum.TimeUnit import TimeUnit  # noqa: E402

from ..schemas import BackupSettings


def to_backup_settings(config) -> BackupSettings:
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


def apply_backup_settings(config, settings: BackupSettings):
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
