from modules.util.enum.GradientReducePrecision import GradientReducePrecision  # noqa: E402
from modules.util.enum.TimeUnit import TimeUnit  # noqa: E402

from ..schemas import GeneralSettings

GENERAL_CONFIG_FIELDS = [
    "workspace_dir",
    "cache_dir",
    "continue_last_backup",
    "only_cache",
    "debug_mode",
    "debug_dir",
    "tensorboard",
    "tensorboard_always_on",
    "tensorboard_expose",
    "tensorboard_port",
    "validation",
    "validate_after",
    "validate_after_unit",
    "dataloader_threads",
    "train_device",
    "multi_gpu",
    "device_indexes",
    "gradient_reduce_precision",
    "fused_gradient_reduce",
    "async_gradient_reduce",
    "async_gradient_reduce_buffer",
    "temp_device",
]


def to_general_settings(config) -> GeneralSettings:
    config_dict = config.to_dict()
    return GeneralSettings.model_validate({k: config_dict[k] for k in GENERAL_CONFIG_FIELDS})


def apply_general_settings(config, settings: GeneralSettings):
    payload = settings.model_dump()
    config.workspace_dir = payload["workspace_dir"]
    config.cache_dir = payload["cache_dir"]
    config.continue_last_backup = payload["continue_last_backup"]
    config.only_cache = payload["only_cache"]
    config.debug_mode = payload["debug_mode"]
    config.debug_dir = payload["debug_dir"]
    config.tensorboard = payload["tensorboard"]
    config.tensorboard_always_on = payload["tensorboard_always_on"]
    config.tensorboard_expose = payload["tensorboard_expose"]
    config.tensorboard_port = payload["tensorboard_port"]
    config.validation = payload["validation"]
    config.validate_after = payload["validate_after"]
    config.validate_after_unit = TimeUnit[payload["validate_after_unit"]]
    config.dataloader_threads = payload["dataloader_threads"]
    config.train_device = payload["train_device"]
    config.multi_gpu = payload["multi_gpu"]
    config.device_indexes = payload["device_indexes"]
    config.gradient_reduce_precision = GradientReducePrecision[payload["gradient_reduce_precision"]]
    config.fused_gradient_reduce = payload["fused_gradient_reduce"]
    config.async_gradient_reduce = payload["async_gradient_reduce"]
    config.async_gradient_reduce_buffer = payload["async_gradient_reduce_buffer"]
    config.temp_device = payload["temp_device"]
    return config
