import { fetchDataConfig, saveDataConfig } from '../../lib/api/client';
import type { DataSettings } from '../../lib/api/types';
import { loadConfigResource, saveConfigResource } from '../../app/configResource';
import { fromDataResponse, toDataSavePayload } from './adapter';

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

type DataLoadArgs = {
  setDataForm: (value: DataSettings) => void;
  markLoaded: () => void;
  stateSetters: LoadStateSetters;
};

type DataSaveArgs = {
  dataForm: DataSettings;
  setDataForm: (value: DataSettings) => void;
  stateSetters: SaveStateSetters;
};

export async function loadDataState(args: DataLoadArgs): Promise<void> {
  const { setDataForm, markLoaded, stateSetters } = args;

  await loadConfigResource({
    request: fetchDataConfig,
    onSuccess: (response) => {
      setDataForm(fromDataResponse(response));
      markLoaded();
    },
    failureMessage: 'Failed to load Data config',
    ...stateSetters
  });
}

export async function saveDataState(args: DataSaveArgs): Promise<void> {
  const { dataForm, setDataForm, stateSetters } = args;

  const payload = toDataSavePayload(dataForm);

  await saveConfigResource({
    request: () => saveDataConfig(payload),
    onSuccess: (response) => {
      setDataForm(response.data);
    },
    successMessage: 'Data settings saved.',
    failureMessage: 'Failed to save Data config',
    ...stateSetters
  });
}
