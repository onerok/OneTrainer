from pydantic import BaseModel, Field

from .common import TimeUnitValue


class BackupSettings(BaseModel):
    backup_after: float = Field(ge=0)
    backup_after_unit: TimeUnitValue
    rolling_backup: bool
    rolling_backup_count: int = Field(ge=1)
    backup_before_save: bool
    save_every: float = Field(ge=0)
    save_every_unit: TimeUnitValue
    save_skip_first: int = Field(ge=0)
    save_filename_prefix: str


class BackupMeta(BaseModel):
    backup_after_units: list[TimeUnitValue]
    save_every_units: list[TimeUnitValue]


class BackupConfigResponse(BaseModel):
    data: BackupSettings
    meta: BackupMeta


class SaveBackupConfigRequest(BaseModel):
    data: BackupSettings
