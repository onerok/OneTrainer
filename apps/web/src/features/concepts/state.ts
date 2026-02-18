import { fetchConceptsConfig, saveConceptsConfig } from '../../lib/api/client';
import type { ConceptsSettings } from '../../lib/api/types';
import { loadConfigResource, saveConfigResource } from '../../app/configResource';
import { fromConceptsResponse, toConceptsSavePayload } from './adapter';

type LoadStateSetters = {
  setLoading: (value: boolean) => void;
  setErrorMessage: (value: string) => void;
  setStatusMessage: (value: string) => void;
};

type SaveStateSetters = {
  setSaving: (value: boolean) => void;
  setErrorMessage: (value: string) => void;
  setStatusMessage: (value: string) => void;
};

type ConceptsLoadArgs = {
  setConceptsForm: (value: ConceptsSettings) => void;
  setConceptTypes: (value: string[]) => void;
  setBalancingStrategies: (value: string[]) => void;
  setPromptSources: (value: string[]) => void;
  markLoaded: () => void;
  stateSetters: LoadStateSetters;
};

type ConceptsSaveArgs = {
  conceptsForm: ConceptsSettings;
  setConceptsForm: (value: ConceptsSettings) => void;
  stateSetters: SaveStateSetters;
};

export async function loadConceptsState(args: ConceptsLoadArgs): Promise<void> {
  const { setConceptsForm, setConceptTypes, setBalancingStrategies, setPromptSources, markLoaded, stateSetters } =
    args;

  await loadConfigResource({
    request: fetchConceptsConfig,
    onSuccess: (response) => {
      const adapted = fromConceptsResponse(response);
      setConceptsForm(adapted.form);
      setConceptTypes(adapted.conceptTypes);
      setBalancingStrategies(adapted.balancingStrategies);
      setPromptSources(adapted.promptSources);
      markLoaded();
    },
    failureMessage: 'Failed to load Concepts config',
    ...stateSetters
  });
}

export async function saveConceptsState(args: ConceptsSaveArgs): Promise<void> {
  const { conceptsForm, setConceptsForm, stateSetters } = args;
  const payload = toConceptsSavePayload(conceptsForm);

  await saveConfigResource({
    request: () => saveConceptsConfig(payload),
    onSuccess: (response) => {
      setConceptsForm(response.data);
    },
    successMessage: 'Concept settings saved.',
    failureMessage: 'Failed to save Concepts config',
    ...stateSetters
  });
}
