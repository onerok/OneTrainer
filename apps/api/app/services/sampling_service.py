from modules.util.enum.AudioFormat import AudioFormat  # noqa: E402
from modules.util.enum.ImageFormat import ImageFormat  # noqa: E402
from modules.util.enum.NoiseScheduler import NoiseScheduler  # noqa: E402
from modules.util.enum.TimeUnit import TimeUnit  # noqa: E402
from modules.util.enum.VideoFormat import VideoFormat  # noqa: E402

from ..core.store import store
from ..mappers.sampling import apply_sampling_settings, to_sampling_settings
from ..schemas import SamplingConfigResponse, SamplingMeta, SamplingSettings


def get_sampling_config() -> SamplingConfigResponse:
    config = store.load()
    return SamplingConfigResponse(
        data=to_sampling_settings(config),
        meta=SamplingMeta(
            sample_after_units=[unit.value for unit in TimeUnit],
            sample_image_formats=[image_format.value for image_format in ImageFormat],
            sample_video_formats=[video_format.value for video_format in VideoFormat],
            sample_audio_formats=[audio_format.value for audio_format in AudioFormat],
            noise_schedulers=[scheduler.value for scheduler in NoiseScheduler],
        ),
    )


def save_sampling_config(settings: SamplingSettings) -> SamplingConfigResponse:
    config = store.load()
    config = apply_sampling_settings(config, settings)
    store.save(config)
    return SamplingConfigResponse(
        data=to_sampling_settings(config),
        meta=SamplingMeta(
            sample_after_units=[unit.value for unit in TimeUnit],
            sample_image_formats=[image_format.value for image_format in ImageFormat],
            sample_video_formats=[video_format.value for video_format in VideoFormat],
            sample_audio_formats=[audio_format.value for audio_format in AudioFormat],
            noise_schedulers=[scheduler.value for scheduler in NoiseScheduler],
        ),
    )
