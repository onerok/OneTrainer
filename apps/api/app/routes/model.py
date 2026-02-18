from fastapi import APIRouter

from modules.util.enum.ConfigPart import ConfigPart  # noqa: E402
from modules.util.enum.DataType import DataType  # noqa: E402
from modules.util.enum.ModelFormat import ModelFormat  # noqa: E402
from modules.util.enum.ModelType import ModelType  # noqa: E402
from modules.util.enum.TrainingMethod import TrainingMethod  # noqa: E402

from ..core.store import store
from ..schemas import (
    ModelConfigResponse,
    ModelMeta,
    ModelPartSettings,
    ModelSettings,
    QuantizationSettings,
    SaveModelConfigRequest,
)

router = APIRouter()

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


def _to_model_settings(config) -> ModelSettings:
    return ModelSettings(
        training_method=config.training_method.value,
        model_type=config.model_type.value,
        huggingface_token=config.secrets.huggingface_token,
        base_model_name=config.base_model_name,
        compile=config.compile,
        unet=ModelPartSettings(
            model_name=config.unet.model_name,
            weight_dtype=config.unet.weight_dtype.value,
        ),
        prior=ModelPartSettings(
            model_name=config.prior.model_name,
            weight_dtype=config.prior.weight_dtype.value,
        ),
        transformer=ModelPartSettings(
            model_name=config.transformer.model_name,
            weight_dtype=config.transformer.weight_dtype.value,
        ),
        text_encoder=ModelPartSettings(
            model_name=config.text_encoder.model_name,
            weight_dtype=config.text_encoder.weight_dtype.value,
        ),
        text_encoder_2=ModelPartSettings(
            model_name=config.text_encoder_2.model_name,
            weight_dtype=config.text_encoder_2.weight_dtype.value,
        ),
        text_encoder_3=ModelPartSettings(
            model_name=config.text_encoder_3.model_name,
            weight_dtype=config.text_encoder_3.weight_dtype.value,
        ),
        text_encoder_4=ModelPartSettings(
            model_name=config.text_encoder_4.model_name,
            weight_dtype=config.text_encoder_4.weight_dtype.value,
        ),
        vae=ModelPartSettings(
            model_name=config.vae.model_name,
            weight_dtype=config.vae.weight_dtype.value,
        ),
        effnet_encoder=ModelPartSettings(
            model_name=config.effnet_encoder.model_name,
            weight_dtype=config.effnet_encoder.weight_dtype.value,
        ),
        decoder=ModelPartSettings(
            model_name=config.decoder.model_name,
            weight_dtype=config.decoder.weight_dtype.value,
        ),
        decoder_text_encoder=ModelPartSettings(
            model_name=config.decoder_text_encoder.model_name,
            weight_dtype=config.decoder_text_encoder.weight_dtype.value,
        ),
        decoder_vqgan=ModelPartSettings(
            model_name=config.decoder_vqgan.model_name,
            weight_dtype=config.decoder_vqgan.weight_dtype.value,
        ),
        quantization=QuantizationSettings(
            layer_filter=config.quantization.layer_filter,
            layer_filter_preset=config.quantization.layer_filter_preset,
            layer_filter_regex=config.quantization.layer_filter_regex,
            svd_dtype=config.quantization.svd_dtype.value,
            svd_rank=config.quantization.svd_rank,
        ),
        output_dtype=config.output_dtype.value,
        output_model_format=config.output_model_format.value,
        output_model_destination=config.output_model_destination,
        include_train_config=config.include_train_config.value,
    )


def _apply_model_settings(config, settings: ModelSettings):
    payload = settings.model_dump()
    config.training_method = TrainingMethod[payload["training_method"]]
    config.model_type = ModelType[payload["model_type"]]
    config.secrets.huggingface_token = payload["huggingface_token"]
    config.base_model_name = payload["base_model_name"]
    config.compile = payload["compile"]

    config.unet.model_name = payload["unet"]["model_name"]
    config.unet.weight_dtype = DataType[payload["unet"]["weight_dtype"]]

    config.prior.model_name = payload["prior"]["model_name"]
    config.prior.weight_dtype = DataType[payload["prior"]["weight_dtype"]]

    config.transformer.model_name = payload["transformer"]["model_name"]
    config.transformer.weight_dtype = DataType[payload["transformer"]["weight_dtype"]]

    config.text_encoder.model_name = payload["text_encoder"]["model_name"]
    config.text_encoder.weight_dtype = DataType[payload["text_encoder"]["weight_dtype"]]

    config.text_encoder_2.model_name = payload["text_encoder_2"]["model_name"]
    config.text_encoder_2.weight_dtype = DataType[payload["text_encoder_2"]["weight_dtype"]]

    config.text_encoder_3.model_name = payload["text_encoder_3"]["model_name"]
    config.text_encoder_3.weight_dtype = DataType[payload["text_encoder_3"]["weight_dtype"]]

    config.text_encoder_4.model_name = payload["text_encoder_4"]["model_name"]
    config.text_encoder_4.weight_dtype = DataType[payload["text_encoder_4"]["weight_dtype"]]

    config.vae.model_name = payload["vae"]["model_name"]
    config.vae.weight_dtype = DataType[payload["vae"]["weight_dtype"]]

    config.effnet_encoder.model_name = payload["effnet_encoder"]["model_name"]
    config.effnet_encoder.weight_dtype = DataType[payload["effnet_encoder"]["weight_dtype"]]

    config.decoder.model_name = payload["decoder"]["model_name"]
    config.decoder.weight_dtype = DataType[payload["decoder"]["weight_dtype"]]

    config.decoder_text_encoder.model_name = payload["decoder_text_encoder"]["model_name"]
    config.decoder_text_encoder.weight_dtype = DataType[payload["decoder_text_encoder"]["weight_dtype"]]

    config.decoder_vqgan.model_name = payload["decoder_vqgan"]["model_name"]
    config.decoder_vqgan.weight_dtype = DataType[payload["decoder_vqgan"]["weight_dtype"]]

    config.quantization.layer_filter = payload["quantization"]["layer_filter"]
    config.quantization.layer_filter_preset = payload["quantization"]["layer_filter_preset"]
    config.quantization.layer_filter_regex = payload["quantization"]["layer_filter_regex"]
    config.quantization.svd_dtype = DataType[payload["quantization"]["svd_dtype"]]
    config.quantization.svd_rank = payload["quantization"]["svd_rank"]

    config.output_dtype = DataType[payload["output_dtype"]]
    config.output_model_format = ModelFormat[payload["output_model_format"]]
    config.output_model_destination = payload["output_model_destination"]
    config.include_train_config = ConfigPart[payload["include_train_config"]]
    return config


@router.get("/api/v1/model-config", response_model=ModelConfigResponse)
def get_model_config() -> ModelConfigResponse:
    config = store.load()
    return ModelConfigResponse(
        data=_to_model_settings(config),
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


@router.post("/api/v1/model-config", response_model=ModelConfigResponse)
def save_model_config(body: SaveModelConfigRequest) -> ModelConfigResponse:
    config = store.load()
    config = _apply_model_settings(config, body.data)
    store.save(config)

    return ModelConfigResponse(
        data=_to_model_settings(config),
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
