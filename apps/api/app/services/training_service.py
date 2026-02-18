from modules.util.enum.DataType import DataType  # noqa: E402
from modules.util.enum.EMAMode import EMAMode  # noqa: E402
from modules.util.enum.GradientCheckpointingMethod import GradientCheckpointingMethod  # noqa: E402
from modules.util.enum.LearningRateScaler import LearningRateScaler  # noqa: E402
from modules.util.enum.LearningRateScheduler import LearningRateScheduler  # noqa: E402
from modules.util.enum.Optimizer import Optimizer  # noqa: E402

from ..core.store import store
from ..mappers.training import apply_training_settings, to_training_settings
from ..schemas import TrainingConfigResponse, TrainingMeta, TrainingSettings

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


def get_training_config() -> TrainingConfigResponse:
    config = store.load()
    return TrainingConfigResponse(
        data=to_training_settings(config),
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


def save_training_config(settings: TrainingSettings) -> TrainingConfigResponse:
    config = store.load()
    config = apply_training_settings(config, settings)
    store.save(config)
    return TrainingConfigResponse(
        data=to_training_settings(config),
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
