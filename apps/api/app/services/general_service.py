from modules.util.enum.GradientReducePrecision import GradientReducePrecision  # noqa: E402
from modules.util.enum.TimeUnit import TimeUnit  # noqa: E402

from ..core.store import store
from ..mappers.general import apply_general_settings, to_general_settings
from ..schemas import GeneralConfigResponse, GeneralMeta, GeneralSettings


def get_general_config() -> GeneralConfigResponse:
    config = store.load()
    return GeneralConfigResponse(
        data=to_general_settings(config),
        meta=GeneralMeta(
            validate_after_units=[unit.value for unit in TimeUnit],
            gradient_reduce_precisions=[precision.value for precision in GradientReducePrecision],
        ),
    )


def save_general_config(settings: GeneralSettings) -> GeneralConfigResponse:
    config = store.load()
    config = apply_general_settings(config, settings)
    store.save(config)
    return GeneralConfigResponse(
        data=to_general_settings(config),
        meta=GeneralMeta(
            validate_after_units=[unit.value for unit in TimeUnit],
            gradient_reduce_precisions=[precision.value for precision in GradientReducePrecision],
        ),
    )
