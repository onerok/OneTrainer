from pydantic import BaseModel, Field

from .common import ConfigPartValue, DataTypeValue, ModelFormatValue, ModelTypeValue, TrainingMethodValue


class ModelPartSettings(BaseModel):
    model_name: str
    weight_dtype: DataTypeValue


class QuantizationSettings(BaseModel):
    layer_filter: str
    layer_filter_preset: str
    layer_filter_regex: bool
    svd_dtype: DataTypeValue
    svd_rank: int = Field(ge=1)


class ModelSettings(BaseModel):
    training_method: TrainingMethodValue
    model_type: ModelTypeValue
    huggingface_token: str
    base_model_name: str
    compile: bool
    unet: ModelPartSettings
    prior: ModelPartSettings
    transformer: ModelPartSettings
    text_encoder: ModelPartSettings
    text_encoder_2: ModelPartSettings
    text_encoder_3: ModelPartSettings
    text_encoder_4: ModelPartSettings
    vae: ModelPartSettings
    effnet_encoder: ModelPartSettings
    decoder: ModelPartSettings
    decoder_text_encoder: ModelPartSettings
    decoder_vqgan: ModelPartSettings
    quantization: QuantizationSettings
    output_dtype: DataTypeValue
    output_model_format: ModelFormatValue
    output_model_destination: str
    include_train_config: ConfigPartValue


class ModelMeta(BaseModel):
    training_methods: list[TrainingMethodValue]
    model_types: list[ModelTypeValue]
    data_types: list[DataTypeValue]
    output_dtypes: list[DataTypeValue]
    model_formats: list[ModelFormatValue]
    include_train_configs: list[ConfigPartValue]
    quantization_presets: list[str]


class ModelConfigResponse(BaseModel):
    data: ModelSettings
    meta: ModelMeta


class SaveModelConfigRequest(BaseModel):
    data: ModelSettings
