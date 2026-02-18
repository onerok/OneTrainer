from pydantic import BaseModel, ConfigDict, Field

from .common import AudioFormatValue, ImageFormatValue, NoiseSchedulerValue, TimeUnitValue, VideoFormatValue


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
