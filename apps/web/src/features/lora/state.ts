import { fetchLoraConfig, saveLoraConfig } from '../../lib/api/client';
import type { LoraSettings } from '../../lib/api/types';
import { loadConfigResource, saveConfigResource } from '../../app/configResource';
import { fromLoraResponse, toLoraSavePayload } from './adapter';

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

type LoraLoadArgs = {
  setLoraForm: (value: LoraSettings) => void;
  setPeftTypes: (value: string[]) => void;
  setLoraWeightDtypes: (value: string[]) => void;
  markLoaded: () => void;
  stateSetters: LoadStateSetters;
};

type LoraSaveArgs = {
  loraForm: LoraSettings;
  setLoraForm: (value: LoraSettings) => void;
  stateSetters: SaveStateSetters;
};

export async function loadLoraState(args: LoraLoadArgs): Promise<void> {
  const { setLoraForm, setPeftTypes, setLoraWeightDtypes, markLoaded, stateSetters } = args;

  await loadConfigResource({
    request: fetchLoraConfig,
    onSuccess: (response) => {
      const adapted = fromLoraResponse(response);
      setLoraForm(adapted.form);
      setPeftTypes(adapted.peftTypes);
      setLoraWeightDtypes(adapted.loraWeightDtypes);
      markLoaded();
    },
    failureMessage: 'Failed to load LoRA config',
    ...stateSetters
  });
}

export async function saveLoraState(args: LoraSaveArgs): Promise<void> {
  const { loraForm, setLoraForm, stateSetters } = args;

  const payload = toLoraSavePayload(loraForm);

  await saveConfigResource({
    request: () => saveLoraConfig(payload),
    onSuccess: (response) => {
      setLoraForm(response.data);
    },
    successMessage: 'LoRA settings saved.',
    failureMessage: 'Failed to save LoRA config',
    ...stateSetters
  });
}
