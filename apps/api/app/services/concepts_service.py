from modules.util.enum.BalancingStrategy import BalancingStrategy  # noqa: E402
from modules.util.enum.ConceptType import ConceptType  # noqa: E402

from ..core.store import store
from ..mappers.concepts import apply_concepts_settings, to_concepts_settings
from ..schemas import ConceptsConfigResponse, ConceptsMeta, ConceptsSettings

PROMPT_SOURCE_OPTIONS = ["sample", "concept", "filename"]


def get_concepts_config() -> ConceptsConfigResponse:
    config = store.load()
    return ConceptsConfigResponse(
        data=to_concepts_settings(config),
        meta=ConceptsMeta(
            concept_types=[item.value for item in ConceptType],
            balancing_strategies=[item.value for item in BalancingStrategy],
            prompt_sources=PROMPT_SOURCE_OPTIONS,
        ),
    )


def save_concepts_config(settings: ConceptsSettings) -> ConceptsConfigResponse:
    config = store.load()
    config = apply_concepts_settings(config, settings)
    store.save(config)
    return ConceptsConfigResponse(
        data=to_concepts_settings(config),
        meta=ConceptsMeta(
            concept_types=[item.value for item in ConceptType],
            balancing_strategies=[item.value for item in BalancingStrategy],
            prompt_sources=PROMPT_SOURCE_OPTIONS,
        ),
    )
