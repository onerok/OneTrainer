from modules.util.enum.DataType import DataType  # noqa: E402
from modules.util.enum.ModelType import PeftType  # noqa: E402

from ..core.store import store
from ..mappers.lora import apply_lora_settings, to_lora_settings
from ..schemas import LoraConfigResponse, LoraMeta, LoraSettings

LORA_WEIGHT_DTYPE_OPTIONS = [
    DataType.FLOAT_32.value,
    DataType.BFLOAT_16.value,
]


def get_lora_config() -> LoraConfigResponse:
    config = store.load()
    return LoraConfigResponse(
        data=to_lora_settings(config),
        meta=LoraMeta(
            peft_types=[peft_type.value for peft_type in PeftType],
            lora_weight_dtypes=LORA_WEIGHT_DTYPE_OPTIONS,
        ),
    )


def save_lora_config(settings: LoraSettings) -> LoraConfigResponse:
    config = store.load()
    config = apply_lora_settings(config, settings)
    store.save(config)
    return LoraConfigResponse(
        data=to_lora_settings(config),
        meta=LoraMeta(
            peft_types=[peft_type.value for peft_type in PeftType],
            lora_weight_dtypes=LORA_WEIGHT_DTYPE_OPTIONS,
        ),
    )
