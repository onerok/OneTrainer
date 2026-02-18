import json

from fastapi import APIRouter

from modules.util.config.SampleConfig import SampleConfig  # noqa: E402
from modules.util.enum.AudioFormat import AudioFormat  # noqa: E402
from modules.util.enum.ImageFormat import ImageFormat  # noqa: E402
from modules.util.enum.NoiseScheduler import NoiseScheduler  # noqa: E402
from modules.util.enum.TimeUnit import TimeUnit  # noqa: E402
from modules.util.enum.VideoFormat import VideoFormat  # noqa: E402

from ..core.store import resolve_repo_path, store
from ..schemas import SamplingConfigResponse, SamplingMeta, SamplingSettings, SaveSamplingConfigRequest

router = APIRouter()


def _load_samples(config) -> list[SampleConfig]:
    samples: list[SampleConfig] = []
    sample_path = resolve_repo_path(config.sample_definition_file_name)
    if not sample_path.exists():
        return samples

    with sample_path.open("r", encoding="utf-8") as f:
        loaded = json.load(f)

    for item in loaded:
        samples.append(SampleConfig.default_values().from_dict(item))
    return samples


def _to_sampling_settings(config) -> SamplingSettings:
    samples = _load_samples(config)
    return SamplingSettings(
        sample_definition_file_name=config.sample_definition_file_name,
        sample_after=config.sample_after,
        sample_after_unit=config.sample_after_unit.value,
        sample_skip_first=config.sample_skip_first,
        sample_image_format=config.sample_image_format.value,
        sample_video_format=config.sample_video_format.value,
        sample_audio_format=config.sample_audio_format.value,
        samples_to_tensorboard=config.samples_to_tensorboard,
        non_ema_sampling=config.non_ema_sampling,
        samples=[item.to_dict() for item in samples],
    )


def _apply_sampling_settings(config, settings: SamplingSettings):
    payload = settings.model_dump()
    config.sample_definition_file_name = payload["sample_definition_file_name"]
    config.sample_after = payload["sample_after"]
    config.sample_after_unit = TimeUnit[payload["sample_after_unit"]]
    config.sample_skip_first = payload["sample_skip_first"]
    config.sample_image_format = ImageFormat[payload["sample_image_format"]]
    config.sample_video_format = VideoFormat[payload["sample_video_format"]]
    config.sample_audio_format = AudioFormat[payload["sample_audio_format"]]
    config.samples_to_tensorboard = payload["samples_to_tensorboard"]
    config.non_ema_sampling = payload["non_ema_sampling"]

    sample_path = resolve_repo_path(config.sample_definition_file_name)
    sample_path.parent.mkdir(parents=True, exist_ok=True)

    normalized_samples = []
    for item in payload["samples"]:
        normalized_samples.append(SampleConfig.default_values().from_dict(item).to_dict())

    with sample_path.open("w", encoding="utf-8") as f:
        json.dump(normalized_samples, f, indent=2)
        f.write("\n")

    config.samples = None
    return config


@router.get("/api/v1/sampling-config", response_model=SamplingConfigResponse)
def get_sampling_config() -> SamplingConfigResponse:
    config = store.load()
    return SamplingConfigResponse(
        data=_to_sampling_settings(config),
        meta=SamplingMeta(
            sample_after_units=[unit.value for unit in TimeUnit],
            sample_image_formats=[image_format.value for image_format in ImageFormat],
            sample_video_formats=[video_format.value for video_format in VideoFormat],
            sample_audio_formats=[audio_format.value for audio_format in AudioFormat],
            noise_schedulers=[scheduler.value for scheduler in NoiseScheduler],
        ),
    )


@router.post("/api/v1/sampling-config", response_model=SamplingConfigResponse)
def save_sampling_config(body: SaveSamplingConfigRequest) -> SamplingConfigResponse:
    config = store.load()
    config = _apply_sampling_settings(config, body.data)
    store.save(config)
    return SamplingConfigResponse(
        data=_to_sampling_settings(config),
        meta=SamplingMeta(
            sample_after_units=[unit.value for unit in TimeUnit],
            sample_image_formats=[image_format.value for image_format in ImageFormat],
            sample_video_formats=[video_format.value for video_format in VideoFormat],
            sample_audio_formats=[audio_format.value for audio_format in AudioFormat],
            noise_schedulers=[scheduler.value for scheduler in NoiseScheduler],
        ),
    )
