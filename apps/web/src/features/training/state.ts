import { fetchTrainingConfig, saveTrainingConfig } from '../../lib/api/client';
import type { TrainingSettings } from '../../lib/api/types';
import { loadConfigResource, saveConfigResource } from '../../app/configResource';
import { fromTrainingResponse, toTrainingSavePayload } from './adapter';

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

type TrainingLoadArgs = {
  setTrainingForm: (value: TrainingSettings) => void;
  setTrainingClipGradNorm: (value: number | '') => void;
  setOptimizers: (value: string[]) => void;
  setLearningRateSchedulers: (value: string[]) => void;
  setLearningRateScalers: (value: string[]) => void;
  setEmaModes: (value: string[]) => void;
  setGradientCheckpointingMethods: (value: string[]) => void;
  setTrainDtypes: (value: string[]) => void;
  setFallbackTrainDtypes: (value: string[]) => void;
  markLoaded: () => void;
  stateSetters: LoadStateSetters;
};

type TrainingSaveArgs = {
  trainingForm: TrainingSettings;
  trainingClipGradNorm: number | '';
  setTrainingForm: (value: TrainingSettings) => void;
  setTrainingClipGradNorm: (value: number | '') => void;
  stateSetters: SaveStateSetters;
};

export async function loadTrainingState(args: TrainingLoadArgs): Promise<void> {
  const {
    setTrainingForm,
    setTrainingClipGradNorm,
    setOptimizers,
    setLearningRateSchedulers,
    setLearningRateScalers,
    setEmaModes,
    setGradientCheckpointingMethods,
    setTrainDtypes,
    setFallbackTrainDtypes,
    markLoaded,
    stateSetters
  } = args;

  await loadConfigResource({
    request: fetchTrainingConfig,
    onSuccess: (response) => {
      const adapted = fromTrainingResponse(response);
      setTrainingForm(adapted.form);
      setTrainingClipGradNorm(adapted.trainingClipGradNorm);
      setOptimizers(adapted.optimizers);
      setLearningRateSchedulers(adapted.learningRateSchedulers);
      setLearningRateScalers(adapted.learningRateScalers);
      setEmaModes(adapted.emaModes);
      setGradientCheckpointingMethods(adapted.gradientCheckpointingMethods);
      setTrainDtypes(adapted.trainDtypes);
      setFallbackTrainDtypes(adapted.fallbackTrainDtypes);
      markLoaded();
    },
    failureMessage: 'Failed to load Training config',
    ...stateSetters
  });
}

export async function saveTrainingState(args: TrainingSaveArgs): Promise<void> {
  const { trainingForm, trainingClipGradNorm, setTrainingForm, setTrainingClipGradNorm, stateSetters } = args;

  const payload = toTrainingSavePayload(trainingForm, trainingClipGradNorm);

  await saveConfigResource({
    request: () => saveTrainingConfig(payload),
    onSuccess: (response) => {
      setTrainingForm(response.data);
      setTrainingClipGradNorm(response.data.clip_grad_norm ?? '');
    },
    successMessage: 'Training settings saved.',
    failureMessage: 'Failed to save Training config',
    ...stateSetters
  });
}
