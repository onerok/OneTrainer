import { fetchBackupConfig, saveBackupConfig } from '../../lib/api/client';
import type { BackupSettings } from '../../lib/api/types';
import { loadConfigResource, saveConfigResource } from '../../app/configResource';
import { fromBackupResponse, toBackupSavePayload } from './adapter';

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

type BackupLoadArgs = {
  setBackupForm: (value: BackupSettings) => void;
  setBackupAfterUnits: (value: string[]) => void;
  setSaveEveryUnits: (value: string[]) => void;
  markLoaded: () => void;
  stateSetters: LoadStateSetters;
};

type BackupSaveArgs = {
  backupForm: BackupSettings;
  setBackupForm: (value: BackupSettings) => void;
  stateSetters: SaveStateSetters;
};

export async function loadBackupState(args: BackupLoadArgs): Promise<void> {
  const { setBackupForm, setBackupAfterUnits, setSaveEveryUnits, markLoaded, stateSetters } = args;

  await loadConfigResource({
    request: fetchBackupConfig,
    onSuccess: (response) => {
      const adapted = fromBackupResponse(response);
      setBackupForm(adapted.form);
      setBackupAfterUnits(adapted.backupAfterUnits);
      setSaveEveryUnits(adapted.saveEveryUnits);
      markLoaded();
    },
    failureMessage: 'Failed to load Backup config',
    ...stateSetters
  });
}

export async function saveBackupState(args: BackupSaveArgs): Promise<void> {
  const { backupForm, setBackupForm, stateSetters } = args;

  const payload = toBackupSavePayload(backupForm);

  await saveConfigResource({
    request: () => saveBackupConfig(payload),
    onSuccess: (response) => {
      setBackupForm(response.data);
    },
    successMessage: 'Backup settings saved.',
    failureMessage: 'Failed to save Backup config',
    ...stateSetters
  });
}
