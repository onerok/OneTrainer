import json

from fastapi import APIRouter

from modules.util.config.ConceptConfig import ConceptConfig  # noqa: E402
from modules.util.enum.BalancingStrategy import BalancingStrategy  # noqa: E402
from modules.util.enum.ConceptType import ConceptType  # noqa: E402

from ..core.store import resolve_repo_path, store
from ..schemas import ConceptsConfigResponse, ConceptsMeta, ConceptsSettings, SaveConceptsConfigRequest

router = APIRouter()

PROMPT_SOURCE_OPTIONS = ["sample", "concept", "filename"]


def _load_concepts(config) -> list[ConceptConfig]:
    concepts: list[ConceptConfig] = []
    concept_path = resolve_repo_path(config.concept_file_name)

    if not concept_path.exists():
        return concepts

    with concept_path.open("r", encoding="utf-8") as f:
        loaded = json.load(f)

    for item in loaded:
        concepts.append(ConceptConfig.default_values().from_dict(item))
    return concepts


def _to_concepts_settings(config) -> ConceptsSettings:
    concepts = _load_concepts(config)
    return ConceptsSettings(
        concept_file_name=config.concept_file_name,
        concepts=[item.to_dict() for item in concepts],
    )


def _apply_concepts_settings(config, settings: ConceptsSettings):
    payload = settings.model_dump()
    config.concept_file_name = payload["concept_file_name"]
    concepts_path = resolve_repo_path(config.concept_file_name)
    concepts_path.parent.mkdir(parents=True, exist_ok=True)

    normalized_concepts = []
    for item in payload["concepts"]:
        normalized_concepts.append(ConceptConfig.default_values().from_dict(item).to_dict())

    with concepts_path.open("w", encoding="utf-8") as f:
        json.dump(normalized_concepts, f, indent=2)
        f.write("\n")
    return config


@router.get("/api/v1/concepts-config", response_model=ConceptsConfigResponse)
def get_concepts_config() -> ConceptsConfigResponse:
    config = store.load()
    return ConceptsConfigResponse(
        data=_to_concepts_settings(config),
        meta=ConceptsMeta(
            concept_types=[item.value for item in ConceptType],
            balancing_strategies=[item.value for item in BalancingStrategy],
            prompt_sources=PROMPT_SOURCE_OPTIONS,
        ),
    )


@router.post("/api/v1/concepts-config", response_model=ConceptsConfigResponse)
def save_concepts_config(body: SaveConceptsConfigRequest) -> ConceptsConfigResponse:
    config = store.load()
    config = _apply_concepts_settings(config, body.data)
    store.save(config)
    return ConceptsConfigResponse(
        data=_to_concepts_settings(config),
        meta=ConceptsMeta(
            concept_types=[item.value for item in ConceptType],
            balancing_strategies=[item.value for item in BalancingStrategy],
            prompt_sources=PROMPT_SOURCE_OPTIONS,
        ),
    )
