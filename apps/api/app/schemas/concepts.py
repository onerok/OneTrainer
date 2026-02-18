from pydantic import BaseModel, ConfigDict, Field

from .common import BalancingStrategyValue, ConceptTypeValue


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
