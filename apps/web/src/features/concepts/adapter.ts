import type { ConceptsConfigResponse, ConceptsSettings } from '../../lib/api/types';

export function fromConceptsResponse(response: ConceptsConfigResponse): {
  form: ConceptsSettings;
  conceptTypes: string[];
  balancingStrategies: string[];
  promptSources: string[];
} {
  return {
    form: response.data,
    conceptTypes: response.meta.concept_types,
    balancingStrategies: response.meta.balancing_strategies,
    promptSources: response.meta.prompt_sources
  };
}

export function toConceptsSavePayload(form: ConceptsSettings): ConceptsSettings {
  return form;
}
