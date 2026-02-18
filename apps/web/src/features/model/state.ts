import { fetchModelConfig, saveModelConfig } from '../../lib/api/client';
import type { ModelSettings } from '../../lib/api/types';
import { loadConfigResource, saveConfigResource } from '../../app/configResource';
import { fromModelResponse, toModelSavePayload } from './adapter';

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

type ModelLoadArgs = {
  setModelForm: (value: ModelSettings) => void;
  setTrainingMethods: (value: string[]) => void;
  setModelTypes: (value: string[]) => void;
  setDataTypes: (value: string[]) => void;
  setOutputDtypes: (value: string[]) => void;
  setModelFormats: (value: string[]) => void;
  setIncludeTrainConfigs: (value: string[]) => void;
  setQuantizationPresets: (value: string[]) => void;
  markLoaded: () => void;
  stateSetters: LoadStateSetters;
};

type ModelSaveArgs = {
  modelForm: ModelSettings;
  setModelForm: (value: ModelSettings) => void;
  stateSetters: SaveStateSetters;
};

export async function loadModelState(args: ModelLoadArgs): Promise<void> {
  const {
    setModelForm,
    setTrainingMethods,
    setModelTypes,
    setDataTypes,
    setOutputDtypes,
    setModelFormats,
    setIncludeTrainConfigs,
    setQuantizationPresets,
    markLoaded,
    stateSetters
  } = args;

  await loadConfigResource({
    request: fetchModelConfig,
    onSuccess: (response) => {
      const adapted = fromModelResponse(response);
      setModelForm(adapted.form);
      setTrainingMethods(adapted.trainingMethods);
      setModelTypes(adapted.modelTypes);
      setDataTypes(adapted.dataTypes);
      setOutputDtypes(adapted.outputDtypes);
      setModelFormats(adapted.modelFormats);
      setIncludeTrainConfigs(adapted.includeTrainConfigs);
      setQuantizationPresets(adapted.quantizationPresets);
      markLoaded();
    },
    failureMessage: 'Failed to load Model config',
    ...stateSetters
  });
}

export async function saveModelState(args: ModelSaveArgs): Promise<void> {
  const { modelForm, setModelForm, stateSetters } = args;

  const payload = toModelSavePayload(modelForm);

  await saveConfigResource({
    request: () => saveModelConfig(payload),
    onSuccess: (response) => {
      setModelForm(response.data);
    },
    successMessage: 'Model settings saved.',
    failureMessage: 'Failed to save Model config',
    ...stateSetters
  });
}
