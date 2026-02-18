<script lang="ts">
  import type { BackupSettings } from '../../lib/api/types';
  import Button from '../../lib/components/ui/Button.svelte';
  import Input from '../../lib/components/ui/Input.svelte';
  import Label from '../../lib/components/ui/Label.svelte';
  import Select from '../../lib/components/ui/Select.svelte';
  import Switch from '../../lib/components/ui/Switch.svelte';

  export let backupForm: BackupSettings;
  export let backupAfterUnits: string[] = [];
  export let saveEveryUnits: string[] = [];
  export let saving = false;
  export let onSubmit: (event: SubmitEvent) => void | Promise<void>;
  export let onReload: () => void | Promise<void>;
</script>

<form class="general-form" on:submit={onSubmit}>
  <div class="field-grid">
    <div class="field-row split-row">
      <div>
        <Label forId="backup_after">Backup after</Label>
        <Input type="number" min={0} step="any" name="backup_after" bind:value={backupForm.backup_after} />
      </div>
      <div>
        <Label forId="backup_after_unit">Unit</Label>
        <Select name="backup_after_unit" bind:value={backupForm.backup_after_unit} options={backupAfterUnits} />
      </div>
    </div>

    <div class="field-row switch-row">
      <Label forId="rolling_backup">Rolling Backup</Label>
      <Switch name="rolling_backup" bind:checked={backupForm.rolling_backup} />
    </div>

    <div class="field-row">
      <Label forId="rolling_backup_count">Rolling Backup Count</Label>
      <Input type="number" min={1} name="rolling_backup_count" bind:value={backupForm.rolling_backup_count} />
    </div>

    <div class="field-row switch-row">
      <Label forId="backup_before_save">Backup Before Save</Label>
      <Switch name="backup_before_save" bind:checked={backupForm.backup_before_save} />
    </div>

    <div class="field-row split-row">
      <div>
        <Label forId="save_every">Save Every</Label>
        <Input type="number" min={0} step="any" name="save_every" bind:value={backupForm.save_every} />
      </div>
      <div>
        <Label forId="save_every_unit">Unit</Label>
        <Select name="save_every_unit" bind:value={backupForm.save_every_unit} options={saveEveryUnits} />
      </div>
    </div>

    <div class="field-row">
      <Label forId="save_skip_first">Skip First</Label>
      <Input type="number" min={0} name="save_skip_first" bind:value={backupForm.save_skip_first} />
    </div>

    <div class="field-row full-width">
      <Label forId="save_filename_prefix">Save Filename Prefix</Label>
      <Input name="save_filename_prefix" bind:value={backupForm.save_filename_prefix} />
    </div>
  </div>

  <div class="action-row">
    <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save Backup Settings'}</Button>
    <Button type="button" disabled={saving} on:click={onReload}>Reload</Button>
  </div>
</form>
