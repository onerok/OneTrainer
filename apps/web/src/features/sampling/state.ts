import { fetchSamplingConfig, saveSamplingConfig } from '../../lib/api/client';
import type { SamplingSettings } from '../../lib/api/types';
import { loadConfigResource, saveConfigResource } from '../../app/configResource';
import { fromSamplingResponse, toSamplingSavePayload } from './adapter';

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

type SamplingLoadArgs = {
  setSamplingForm: (value: SamplingSettings) => void;
  setSampleAfterUnits: (value: string[]) => void;
  setSampleImageFormats: (value: string[]) => void;
  setSampleVideoFormats: (value: string[]) => void;
  setSampleAudioFormats: (value: string[]) => void;
  setNoiseSchedulers: (value: string[]) => void;
  markLoaded: () => void;
  stateSetters: LoadStateSetters;
};

type SamplingSaveArgs = {
  samplingForm: SamplingSettings;
  setSamplingForm: (value: SamplingSettings) => void;
  stateSetters: SaveStateSetters;
};

export async function loadSamplingState(args: SamplingLoadArgs): Promise<void> {
  const {
    setSamplingForm,
    setSampleAfterUnits,
    setSampleImageFormats,
    setSampleVideoFormats,
    setSampleAudioFormats,
    setNoiseSchedulers,
    markLoaded,
    stateSetters
  } = args;

  await loadConfigResource({
    request: fetchSamplingConfig,
    onSuccess: (response) => {
      const adapted = fromSamplingResponse(response);
      setSamplingForm(adapted.form);
      setSampleAfterUnits(adapted.sampleAfterUnits);
      setSampleImageFormats(adapted.sampleImageFormats);
      setSampleVideoFormats(adapted.sampleVideoFormats);
      setSampleAudioFormats(adapted.sampleAudioFormats);
      setNoiseSchedulers(adapted.noiseSchedulers);
      markLoaded();
    },
    failureMessage: 'Failed to load Sampling config',
    ...stateSetters
  });
}

export async function saveSamplingState(args: SamplingSaveArgs): Promise<void> {
  const { samplingForm, setSamplingForm, stateSetters } = args;

  const payload = toSamplingSavePayload(samplingForm);

  await saveConfigResource({
    request: () => saveSamplingConfig(payload),
    onSuccess: (response) => {
      setSamplingForm(response.data);
    },
    successMessage: 'Sampling settings saved.',
    failureMessage: 'Failed to save Sampling config',
    ...stateSetters
  });
}
