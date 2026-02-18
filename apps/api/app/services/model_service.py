from modules.util.enum.ConfigPart import ConfigPart  # noqa: E402
from modules.util.enum.DataType import DataType  # noqa: E402
from modules.util.enum.ModelFormat import ModelFormat  # noqa: E402
from modules.util.enum.ModelType import ModelType  # noqa: E402
from modules.util.enum.TrainingMethod import TrainingMethod  # noqa: E402

from ..core.store import store
from ..mappers.model import apply_model_settings, to_model_settings
from ..schemas import ModelConfigResponse, ModelMeta, ModelSettings

MODEL_QUANTIZATION_PRESETS = ["full", "none"]

MODEL_DTYPE_OPTIONS = [
    DataType.FLOAT_32.value,
    DataType.BFLOAT_16.value,
    DataType.FLOAT_16.value,
    DataType.FLOAT_8.value,
    DataType.NFLOAT_4.value,
    DataType.FLOAT_W8A8.value,
    DataType.INT_W8A8.value,
    DataType.GGUF.value,
    DataType.GGUF_A8_FLOAT.value,
    DataType.GGUF_A8_INT.value,
]

OUTPUT_DTYPE_OPTIONS = [
    DataType.FLOAT_16.value,
    DataType.FLOAT_32.value,
    DataType.BFLOAT_16.value,
    DataType.FLOAT_8.value,
    DataType.NFLOAT_4.value,
]


def get_model_config() -> ModelConfigResponse:
    config = store.load()
    return ModelConfigResponse(
        data=to_model_settings(config),
        meta=ModelMeta(
            training_methods=[method.value for method in TrainingMethod],
            model_types=[model.value for model in ModelType],
            data_types=MODEL_DTYPE_OPTIONS,
            output_dtypes=OUTPUT_DTYPE_OPTIONS,
            model_formats=[model_format.value for model_format in ModelFormat],
            include_train_configs=[config_part.value for config_part in ConfigPart],
            quantization_presets=MODEL_QUANTIZATION_PRESETS,
        ),
    )


def save_model_config(settings: ModelSettings) -> ModelConfigResponse:
    config = store.load()
    config = apply_model_settings(config, settings)
    store.save(config)
    return ModelConfigResponse(
        data=to_model_settings(config),
        meta=ModelMeta(
            training_methods=[method.value for method in TrainingMethod],
            model_types=[model.value for model in ModelType],
            data_types=MODEL_DTYPE_OPTIONS,
            output_dtypes=OUTPUT_DTYPE_OPTIONS,
            model_formats=[model_format.value for model_format in ModelFormat],
            include_train_configs=[config_part.value for config_part in ConfigPart],
            quantization_presets=MODEL_QUANTIZATION_PRESETS,
        ),
    )
