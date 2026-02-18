import { fetchGeneralConfig, saveGeneralConfig } from '../../lib/api/client';
import type { GeneralSettings } from '../../lib/api/types';
import { loadConfigResource, saveConfigResource } from '../../app/configResource';
import { fromGeneralResponse, toGeneralSavePayload } from './adapter';

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

type GeneralLoadArgs = {
  setGeneralForm: (value: GeneralSettings) => void;
  setValidateAfterUnits: (value: string[]) => void;
  setGradientReducePrecisions: (value: string[]) => void;
  markLoaded: () => void;
  stateSetters: LoadStateSetters;
};

type GeneralSaveArgs = {
  generalForm: GeneralSettings;
  setGeneralForm: (value: GeneralSettings) => void;
  stateSetters: SaveStateSetters;
};

export async function loadGeneralState(args: GeneralLoadArgs): Promise<void> {
  const { setGeneralForm, setValidateAfterUnits, setGradientReducePrecisions, markLoaded, stateSetters } = args;

  await loadConfigResource({
    request: fetchGeneralConfig,
    onSuccess: (response) => {
      const adapted = fromGeneralResponse(response);
      setGeneralForm(adapted.form);
      setValidateAfterUnits(adapted.validateAfterUnits);
      setGradientReducePrecisions(adapted.gradientReducePrecisions);
      markLoaded();
    },
    failureMessage: 'Failed to load General config',
    ...stateSetters
  });
}

export async function saveGeneralState(args: GeneralSaveArgs): Promise<void> {
  const { generalForm, setGeneralForm, stateSetters } = args;

  const payload = toGeneralSavePayload(generalForm);

  await saveConfigResource({
    request: () => saveGeneralConfig(payload),
    onSuccess: (response) => {
      setGeneralForm(response.data);
    },
    successMessage: 'General settings saved.',
    failureMessage: 'Failed to save General config',
    ...stateSetters
  });
}
