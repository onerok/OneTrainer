import type { BackupConfigResponse, BackupSettings } from '../../lib/api/types';

export function fromBackupResponse(response: BackupConfigResponse): {
  form: BackupSettings;
  backupAfterUnits: string[];
  saveEveryUnits: string[];
} {
  return {
    form: response.data,
    backupAfterUnits: response.meta.backup_after_units,
    saveEveryUnits: response.meta.save_every_units
  };
}

export function toBackupSavePayload(form: BackupSettings): BackupSettings {
  return {
    ...form,
    backup_after: Number(form.backup_after),
    rolling_backup_count: Number(form.rolling_backup_count),
    save_every: Number(form.save_every),
    save_skip_first: Number(form.save_skip_first)
  };
}
