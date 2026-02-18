from modules.util.enum.DataType import DataType  # noqa: E402
from modules.util.enum.ModelType import PeftType  # noqa: E402

from ..schemas import LoraSettings


def to_lora_settings(config) -> LoraSettings:
    return LoraSettings(
        peft_type=config.peft_type.value,
        lora_model_name=config.lora_model_name,
        lora_rank=config.lora_rank,
        lora_alpha=config.lora_alpha,
        lora_decompose=config.lora_decompose,
        lora_decompose_norm_epsilon=config.lora_decompose_norm_epsilon,
        lora_decompose_output_axis=config.lora_decompose_output_axis,
        lora_weight_dtype=config.lora_weight_dtype.value,
        bundle_additional_embeddings=config.bundle_additional_embeddings,
        dropout_probability=config.dropout_probability,
        oft_block_size=config.oft_block_size,
        oft_coft=config.oft_coft,
        coft_eps=config.coft_eps,
        oft_block_share=config.oft_block_share,
    )


def apply_lora_settings(config, settings: LoraSettings):
    payload = settings.model_dump()
    config.peft_type = PeftType[payload["peft_type"]]
    config.lora_model_name = payload["lora_model_name"]
    config.lora_rank = payload["lora_rank"]
    config.lora_alpha = payload["lora_alpha"]
    config.lora_decompose = payload["lora_decompose"]
    config.lora_decompose_norm_epsilon = payload["lora_decompose_norm_epsilon"]
    config.lora_decompose_output_axis = payload["lora_decompose_output_axis"]
    config.lora_weight_dtype = DataType[payload["lora_weight_dtype"]]
    config.bundle_additional_embeddings = payload["bundle_additional_embeddings"]
    config.dropout_probability = payload["dropout_probability"]
    config.oft_block_size = payload["oft_block_size"]
    config.oft_coft = payload["oft_coft"]
    config.coft_eps = payload["coft_eps"]
    config.oft_block_share = payload["oft_block_share"]
    return config
