import json

from modules.util.config.ConceptConfig import ConceptConfig  # noqa: E402

from ..core.store import resolve_repo_path
from ..schemas import ConceptsSettings


def load_concepts(config) -> list[ConceptConfig]:
    concepts: list[ConceptConfig] = []
    concept_path = resolve_repo_path(config.concept_file_name)

    if not concept_path.exists():
        return concepts

    with concept_path.open("r", encoding="utf-8") as f:
        loaded = json.load(f)

    for item in loaded:
        concepts.append(ConceptConfig.default_values().from_dict(item))
    return concepts


def to_concepts_settings(config) -> ConceptsSettings:
    concepts = load_concepts(config)
    return ConceptsSettings(
        concept_file_name=config.concept_file_name,
        concepts=[item.to_dict() for item in concepts],
    )


def apply_concepts_settings(config, settings: ConceptsSettings):
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
