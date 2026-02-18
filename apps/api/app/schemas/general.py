from pydantic import BaseModel, Field

from .common import GradientReducePrecisionValue, TimeUnitValue


class GeneralSettings(BaseModel):
    workspace_dir: str
    cache_dir: str
    continue_last_backup: bool
    only_cache: bool
    debug_mode: bool
    debug_dir: str
    tensorboard: bool
    tensorboard_always_on: bool
    tensorboard_expose: bool
    tensorboard_port: int = Field(ge=1, le=65535)
    validation: bool
    validate_after: float = Field(ge=0)
    validate_after_unit: TimeUnitValue
    dataloader_threads: int = Field(ge=0)
    train_device: str
    multi_gpu: bool
    device_indexes: str
    gradient_reduce_precision: GradientReducePrecisionValue
    fused_gradient_reduce: bool
    async_gradient_reduce: bool
    async_gradient_reduce_buffer: int = Field(ge=0)
    temp_device: str


class GeneralMeta(BaseModel):
    validate_after_units: list[TimeUnitValue]
    gradient_reduce_precisions: list[GradientReducePrecisionValue]


class GeneralConfigResponse(BaseModel):
    data: GeneralSettings
    meta: GeneralMeta


class SaveGeneralConfigRequest(BaseModel):
    data: GeneralSettings
