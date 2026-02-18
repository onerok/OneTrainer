from pydantic import BaseModel, Field

from .common import (
    DataTypeValue,
    EMAModeValue,
    GradientCheckpointingMethodValue,
    LearningRateScalerValue,
    LearningRateSchedulerValue,
)


class TrainingSettings(BaseModel):
    optimizer: str
    learning_rate_scheduler: LearningRateSchedulerValue
    learning_rate: float = Field(ge=0)
    learning_rate_warmup_steps: float = Field(ge=0)
    learning_rate_min_factor: float = Field(ge=0)
    learning_rate_cycles: float = Field(ge=0)
    epochs: int = Field(ge=1)
    batch_size: int = Field(ge=1)
    gradient_accumulation_steps: int = Field(ge=1)
    learning_rate_scaler: LearningRateScalerValue
    clip_grad_norm: float | None = Field(default=None, ge=0)
    ema: EMAModeValue
    ema_decay: float = Field(ge=0, le=1)
    ema_update_step_interval: int = Field(ge=1)
    gradient_checkpointing: GradientCheckpointingMethodValue
    layer_offload_fraction: float = Field(ge=0, le=1)
    train_dtype: DataTypeValue
    fallback_train_dtype: DataTypeValue
    enable_autocast_cache: bool
    resolution: str
    force_circular_padding: bool


class TrainingMeta(BaseModel):
    optimizers: list[str]
    learning_rate_schedulers: list[LearningRateSchedulerValue]
    learning_rate_scalers: list[LearningRateScalerValue]
    ema_modes: list[EMAModeValue]
    gradient_checkpointing_methods: list[GradientCheckpointingMethodValue]
    train_dtypes: list[DataTypeValue]
    fallback_train_dtypes: list[DataTypeValue]


class TrainingConfigResponse(BaseModel):
    data: TrainingSettings
    meta: TrainingMeta


class SaveTrainingConfigRequest(BaseModel):
    data: TrainingSettings
