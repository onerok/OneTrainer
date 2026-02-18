from enum import Enum

from pydantic import BaseModel, Field

from .common import DataTypeValue


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
