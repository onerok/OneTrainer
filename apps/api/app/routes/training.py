from fastapi import APIRouter

from modules.util.enum.DataType import DataType  # noqa: E402
from modules.util.enum.EMAMode import EMAMode  # noqa: E402
from modules.util.enum.GradientCheckpointingMethod import GradientCheckpointingMethod  # noqa: E402
from modules.util.enum.LearningRateScaler import LearningRateScaler  # noqa: E402
from modules.util.enum.LearningRateScheduler import LearningRateScheduler  # noqa: E402
from modules.util.enum.Optimizer import Optimizer  # noqa: E402

from ..core.store import store
from ..schemas import SaveTrainingConfigRequest, TrainingConfigResponse, TrainingMeta, TrainingSettings

router = APIRouter()

TRAIN_DTYPE_OPTIONS = [
    DataType.FLOAT_32.value,
    DataType.FLOAT_16.value,
    DataType.BFLOAT_16.value,
    DataType.TFLOAT_32.value,
]

FALLBACK_TRAIN_DTYPE_OPTIONS = [
    DataType.FLOAT_32.value,
    DataType.BFLOAT_16.value,
]


def _to_training_settings(config) -> TrainingSettings:
    return TrainingSettings(
        optimizer=config.optimizer.optimizer.value,
        learning_rate_scheduler=config.learning_rate_scheduler.value,
        learning_rate=config.learning_rate,
        learning_rate_warmup_steps=config.learning_rate_warmup_steps,
        learning_rate_min_factor=config.learning_rate_min_factor,
        learning_rate_cycles=config.learning_rate_cycles,
        epochs=config.epochs,
        batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate_scaler=config.learning_rate_scaler.value,
        clip_grad_norm=config.clip_grad_norm,
        ema=config.ema.value,
        ema_decay=config.ema_decay,
        ema_update_step_interval=config.ema_update_step_interval,
        gradient_checkpointing=config.gradient_checkpointing.value,
        layer_offload_fraction=config.layer_offload_fraction,
        train_dtype=config.train_dtype.value,
        fallback_train_dtype=config.fallback_train_dtype.value,
        enable_autocast_cache=config.enable_autocast_cache,
        resolution=config.resolution,
        force_circular_padding=config.force_circular_padding,
    )


def _apply_training_settings(config, settings: TrainingSettings):
    payload = settings.model_dump()
    config.optimizer.optimizer = Optimizer[payload["optimizer"]]
    config.learning_rate_scheduler = LearningRateScheduler[payload["learning_rate_scheduler"]]
    config.learning_rate = payload["learning_rate"]
    config.learning_rate_warmup_steps = payload["learning_rate_warmup_steps"]
    config.learning_rate_min_factor = payload["learning_rate_min_factor"]
    config.learning_rate_cycles = payload["learning_rate_cycles"]
    config.epochs = payload["epochs"]
    config.batch_size = payload["batch_size"]
    config.gradient_accumulation_steps = payload["gradient_accumulation_steps"]
    config.learning_rate_scaler = LearningRateScaler[payload["learning_rate_scaler"]]
    config.clip_grad_norm = payload["clip_grad_norm"]
    config.ema = EMAMode[payload["ema"]]
    config.ema_decay = payload["ema_decay"]
    config.ema_update_step_interval = payload["ema_update_step_interval"]
    config.gradient_checkpointing = GradientCheckpointingMethod[payload["gradient_checkpointing"]]
    config.layer_offload_fraction = payload["layer_offload_fraction"]
    config.train_dtype = DataType[payload["train_dtype"]]
    config.fallback_train_dtype = DataType[payload["fallback_train_dtype"]]
    config.enable_autocast_cache = payload["enable_autocast_cache"]
    config.resolution = payload["resolution"]
    config.force_circular_padding = payload["force_circular_padding"]
    return config


@router.get("/api/v1/training-config", response_model=TrainingConfigResponse)
def get_training_config() -> TrainingConfigResponse:
    config = store.load()
    return TrainingConfigResponse(
        data=_to_training_settings(config),
        meta=TrainingMeta(
            optimizers=[optimizer.value for optimizer in Optimizer],
            learning_rate_schedulers=[scheduler.value for scheduler in LearningRateScheduler],
            learning_rate_scalers=[scaler.value for scaler in LearningRateScaler],
            ema_modes=[mode.value for mode in EMAMode],
            gradient_checkpointing_methods=[method.value for method in GradientCheckpointingMethod],
            train_dtypes=TRAIN_DTYPE_OPTIONS,
            fallback_train_dtypes=FALLBACK_TRAIN_DTYPE_OPTIONS,
        ),
    )


@router.post("/api/v1/training-config", response_model=TrainingConfigResponse)
def save_training_config(body: SaveTrainingConfigRequest) -> TrainingConfigResponse:
    config = store.load()
    config = _apply_training_settings(config, body.data)
    store.save(config)
    return TrainingConfigResponse(
        data=_to_training_settings(config),
        meta=TrainingMeta(
            optimizers=[optimizer.value for optimizer in Optimizer],
            learning_rate_schedulers=[scheduler.value for scheduler in LearningRateScheduler],
            learning_rate_scalers=[scaler.value for scaler in LearningRateScaler],
            ema_modes=[mode.value for mode in EMAMode],
            gradient_checkpointing_methods=[method.value for method in GradientCheckpointingMethod],
            train_dtypes=TRAIN_DTYPE_OPTIONS,
            fallback_train_dtypes=FALLBACK_TRAIN_DTYPE_OPTIONS,
        ),
    )
