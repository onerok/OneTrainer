from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TimeUnitValue(str, Enum):
    EPOCH = "EPOCH"
    STEP = "STEP"
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    NEVER = "NEVER"
    ALWAYS = "ALWAYS"


class GradientReducePrecisionValue(str, Enum):
    WEIGHT_DTYPE = "WEIGHT_DTYPE"
    FLOAT_32 = "FLOAT_32"
    WEIGHT_DTYPE_STOCHASTIC = "WEIGHT_DTYPE_STOCHASTIC"
    FLOAT_32_STOCHASTIC = "FLOAT_32_STOCHASTIC"


class LearningRateSchedulerValue(str, Enum):
    CONSTANT = "CONSTANT"
    LINEAR = "LINEAR"
    COSINE = "COSINE"
    COSINE_WITH_RESTARTS = "COSINE_WITH_RESTARTS"
    COSINE_WITH_HARD_RESTARTS = "COSINE_WITH_HARD_RESTARTS"
    REX = "REX"
    ADAFACTOR = "ADAFACTOR"
    CUSTOM = "CUSTOM"


class LearningRateScalerValue(str, Enum):
    NONE = "NONE"
    BATCH = "BATCH"
    GLOBAL_BATCH = "GLOBAL_BATCH"
    GRADIENT_ACCUMULATION = "GRADIENT_ACCUMULATION"
    BOTH = "BOTH"
    GLOBAL_BOTH = "GLOBAL_BOTH"


class EMAModeValue(str, Enum):
    OFF = "OFF"
    GPU = "GPU"
    CPU = "CPU"


class GradientCheckpointingMethodValue(str, Enum):
    OFF = "OFF"
    ON = "ON"
    CPU_OFFLOADED = "CPU_OFFLOADED"


class TrainingMethodValue(str, Enum):
    FINE_TUNE = "FINE_TUNE"
    LORA = "LORA"
    EMBEDDING = "EMBEDDING"
    FINE_TUNE_VAE = "FINE_TUNE_VAE"


class ModelTypeValue(str, Enum):
    STABLE_DIFFUSION_15 = "STABLE_DIFFUSION_15"
    STABLE_DIFFUSION_15_INPAINTING = "STABLE_DIFFUSION_15_INPAINTING"
    STABLE_DIFFUSION_20 = "STABLE_DIFFUSION_20"
    STABLE_DIFFUSION_20_BASE = "STABLE_DIFFUSION_20_BASE"
    STABLE_DIFFUSION_20_INPAINTING = "STABLE_DIFFUSION_20_INPAINTING"
    STABLE_DIFFUSION_20_DEPTH = "STABLE_DIFFUSION_20_DEPTH"
    STABLE_DIFFUSION_21 = "STABLE_DIFFUSION_21"
    STABLE_DIFFUSION_21_BASE = "STABLE_DIFFUSION_21_BASE"
    STABLE_DIFFUSION_3 = "STABLE_DIFFUSION_3"
    STABLE_DIFFUSION_35 = "STABLE_DIFFUSION_35"
    STABLE_DIFFUSION_XL_10_BASE = "STABLE_DIFFUSION_XL_10_BASE"
    STABLE_DIFFUSION_XL_10_BASE_INPAINTING = "STABLE_DIFFUSION_XL_10_BASE_INPAINTING"
    WUERSTCHEN_2 = "WUERSTCHEN_2"
    STABLE_CASCADE_1 = "STABLE_CASCADE_1"
    PIXART_ALPHA = "PIXART_ALPHA"
    PIXART_SIGMA = "PIXART_SIGMA"
    FLUX_DEV_1 = "FLUX_DEV_1"
    FLUX_FILL_DEV_1 = "FLUX_FILL_DEV_1"
    FLUX_2 = "FLUX_2"
    SANA = "SANA"
    HUNYUAN_VIDEO = "HUNYUAN_VIDEO"
    HI_DREAM_FULL = "HI_DREAM_FULL"
    CHROMA_1 = "CHROMA_1"
    QWEN = "QWEN"
    Z_IMAGE = "Z_IMAGE"


class DataTypeValue(str, Enum):
    NONE = "NONE"
    FLOAT_8 = "FLOAT_8"
    FLOAT_16 = "FLOAT_16"
    FLOAT_32 = "FLOAT_32"
    BFLOAT_16 = "BFLOAT_16"
    TFLOAT_32 = "TFLOAT_32"
    INT_8 = "INT_8"
    NFLOAT_4 = "NFLOAT_4"
    FLOAT_W8A8 = "FLOAT_W8A8"
    INT_W8A8 = "INT_W8A8"
    GGUF = "GGUF"
    GGUF_A8_FLOAT = "GGUF_A8_FLOAT"
    GGUF_A8_INT = "GGUF_A8_INT"


class ImageFormatValue(str, Enum):
    PNG = "PNG"
    JPG = "JPG"


class VideoFormatValue(str, Enum):
    PNG_IMAGE_SEQUENCE = "PNG_IMAGE_SEQUENCE"
    JPG_IMAGE_SEQUENCE = "JPG_IMAGE_SEQUENCE"
    MP4 = "MP4"


class AudioFormatValue(str, Enum):
    MP3 = "MP3"


class NoiseSchedulerValue(str, Enum):
    DDIM = "DDIM"
    EULER = "EULER"
    EULER_A = "EULER_A"
    DPMPP = "DPMPP"
    DPMPP_SDE = "DPMPP_SDE"
    UNIPC = "UNIPC"
    EULER_KARRAS = "EULER_KARRAS"
    DPMPP_KARRAS = "DPMPP_KARRAS"
    DPMPP_SDE_KARRAS = "DPMPP_SDE_KARRAS"
    UNIPC_KARRAS = "UNIPC_KARRAS"


class ModelFormatValue(str, Enum):
    DIFFUSERS = "DIFFUSERS"
    CKPT = "CKPT"
    SAFETENSORS = "SAFETENSORS"
    LEGACY_SAFETENSORS = "LEGACY_SAFETENSORS"
    COMFY_LORA = "COMFY_LORA"
    INTERNAL = "INTERNAL"


class ConfigPartValue(str, Enum):
    NONE = "NONE"
    SETTINGS = "SETTINGS"
    ALL = "ALL"


class ConceptTypeValue(str, Enum):
    STANDARD = "STANDARD"
    VALIDATION = "VALIDATION"
    PRIOR_PREDICTION = "PRIOR_PREDICTION"


class BalancingStrategyValue(str, Enum):
    REPEATS = "REPEATS"
    SAMPLES = "SAMPLES"


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


class DataSettings(BaseModel):
    aspect_ratio_bucketing: bool
    latent_caching: bool
    clear_cache_before_training: bool


class DataConfigResponse(BaseModel):
    data: DataSettings


class SaveDataConfigRequest(BaseModel):
    data: DataSettings


class ToolActionTypeValue(str, Enum):
    WEB_LINK = "WEB_LINK"
    CLI_COMMAND = "CLI_COMMAND"
    INFO = "INFO"


class ToolInfo(BaseModel):
    id: str
    name: str
    description: str
    action_type: ToolActionTypeValue
    action_value: str
    desktop_equivalent: bool


class ToolsConfigResponse(BaseModel):
    data: dict[str, list[ToolInfo]]


class PeftTypeValue(str, Enum):
    LORA = "LORA"
    LOHA = "LOHA"
    OFT_2 = "OFT_2"


class LoraSettings(BaseModel):
    peft_type: PeftTypeValue
    lora_model_name: str
    lora_rank: int = Field(ge=1)
    lora_alpha: float = Field(ge=0)
    lora_decompose: bool
    lora_decompose_norm_epsilon: bool
    lora_decompose_output_axis: bool
    lora_weight_dtype: DataTypeValue
    bundle_additional_embeddings: bool
    dropout_probability: float = Field(ge=0, le=1)
    oft_block_size: int = Field(ge=1)
    oft_coft: bool
    coft_eps: float = Field(ge=0)
    oft_block_share: bool


class LoraMeta(BaseModel):
    peft_types: list[PeftTypeValue]
    lora_weight_dtypes: list[DataTypeValue]


class LoraConfigResponse(BaseModel):
    data: LoraSettings
    meta: LoraMeta


class SaveLoraConfigRequest(BaseModel):
    data: LoraSettings


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


class SamplingSampleSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool
    prompt: str
    negative_prompt: str
    height: int = Field(ge=1)
    width: int = Field(ge=1)
    frames: int = Field(ge=1)
    length: float = Field(ge=0)
    seed: int
    random_seed: bool
    diffusion_steps: int = Field(ge=1)
    cfg_scale: float = Field(ge=0)
    noise_scheduler: NoiseSchedulerValue
    text_encoder_1_layer_skip: int = Field(ge=0)
    text_encoder_1_sequence_length: int | None = Field(default=None, ge=1)
    text_encoder_2_layer_skip: int = Field(ge=0)
    text_encoder_2_sequence_length: int | None = Field(default=None, ge=1)
    text_encoder_3_layer_skip: int = Field(ge=0)
    text_encoder_4_layer_skip: int = Field(ge=0)
    transformer_attention_mask: bool
    force_last_timestep: bool
    sample_inpainting: bool
    base_image_path: str
    mask_image_path: str


class SamplingSettings(BaseModel):
    sample_definition_file_name: str
    sample_after: float = Field(ge=0)
    sample_after_unit: TimeUnitValue
    sample_skip_first: int = Field(ge=0)
    sample_image_format: ImageFormatValue
    sample_video_format: VideoFormatValue
    sample_audio_format: AudioFormatValue
    samples_to_tensorboard: bool
    non_ema_sampling: bool
    samples: list[SamplingSampleSettings]


class SamplingMeta(BaseModel):
    sample_after_units: list[TimeUnitValue]
    sample_image_formats: list[ImageFormatValue]
    sample_video_formats: list[VideoFormatValue]
    sample_audio_formats: list[AudioFormatValue]
    noise_schedulers: list[NoiseSchedulerValue]


class SamplingConfigResponse(BaseModel):
    data: SamplingSettings
    meta: SamplingMeta


class SaveSamplingConfigRequest(BaseModel):
    data: SamplingSettings


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


class ConceptTextSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    prompt_source: str
    prompt_path: str


class ConceptSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    path: str
    enabled: bool
    type: ConceptTypeValue
    include_subdirectories: bool
    image_variations: int = Field(ge=1)
    text_variations: int = Field(ge=1)
    balancing: float = Field(ge=0)
    balancing_strategy: BalancingStrategyValue
    loss_weight: float = Field(ge=0)
    text: ConceptTextSettings


class ConceptsSettings(BaseModel):
    concept_file_name: str
    concepts: list[ConceptSettings]


class ConceptsMeta(BaseModel):
    concept_types: list[ConceptTypeValue]
    balancing_strategies: list[BalancingStrategyValue]
    prompt_sources: list[str]


class ConceptsConfigResponse(BaseModel):
    data: ConceptsSettings
    meta: ConceptsMeta


class SaveConceptsConfigRequest(BaseModel):
    data: ConceptsSettings
