<script lang="ts">
  import type { GeneralSettings } from '../../lib/api/types';
  import Button from '../../lib/components/ui/Button.svelte';
  import Input from '../../lib/components/ui/Input.svelte';
  import Label from '../../lib/components/ui/Label.svelte';
  import Select from '../../lib/components/ui/Select.svelte';
  import Switch from '../../lib/components/ui/Switch.svelte';

  export let generalForm: GeneralSettings;
  export let validateAfterUnits: string[] = [];
  export let gradientReducePrecisions: string[] = [];
  export let saving = false;
  export let onSubmit: (event: SubmitEvent) => void | Promise<void>;
  export let onReload: () => void | Promise<void>;
</script>

<form class="general-form" on:submit={onSubmit}>
  <div class="field-grid">
    <div class="field-row full-width">
      <Label forId="workspace_dir">Workspace Directory</Label>
      <Input name="workspace_dir" bind:value={generalForm.workspace_dir} />
    </div>

    <div class="field-row full-width">
      <Label forId="cache_dir">Cache Directory</Label>
      <Input name="cache_dir" bind:value={generalForm.cache_dir} />
    </div>

    <div class="field-row switch-row">
      <Label forId="continue_last_backup">Continue from last backup</Label>
      <Switch name="continue_last_backup" bind:checked={generalForm.continue_last_backup} />
    </div>

    <div class="field-row switch-row">
      <Label forId="only_cache">Only Cache</Label>
      <Switch name="only_cache" bind:checked={generalForm.only_cache} />
    </div>

    <div class="field-row switch-row">
      <Label forId="debug_mode">Debug mode</Label>
      <Switch name="debug_mode" bind:checked={generalForm.debug_mode} />
    </div>

    <div class="field-row">
      <Label forId="debug_dir">Debug Directory</Label>
      <Input name="debug_dir" bind:value={generalForm.debug_dir} />
    </div>

    <div class="field-row switch-row">
      <Label forId="tensorboard">Tensorboard</Label>
      <Switch name="tensorboard" bind:checked={generalForm.tensorboard} />
    </div>

    <div class="field-row switch-row">
      <Label forId="tensorboard_always_on">Always-On Tensorboard</Label>
      <Switch name="tensorboard_always_on" bind:checked={generalForm.tensorboard_always_on} />
    </div>

    <div class="field-row switch-row">
      <Label forId="tensorboard_expose">Expose Tensorboard</Label>
      <Switch name="tensorboard_expose" bind:checked={generalForm.tensorboard_expose} />
    </div>

    <div class="field-row">
      <Label forId="tensorboard_port">Tensorboard Port</Label>
      <Input type="number" min={1} max={65535} name="tensorboard_port" bind:value={generalForm.tensorboard_port} />
    </div>

    <div class="field-row switch-row">
      <Label forId="validation">Validation</Label>
      <Switch name="validation" bind:checked={generalForm.validation} />
    </div>

    <div class="field-row split-row">
      <div>
        <Label forId="validate_after">Validate after</Label>
        <Input type="number" min={0} name="validate_after" bind:value={generalForm.validate_after} />
      </div>
      <div>
        <Label forId="validate_after_unit">Unit</Label>
        <Select name="validate_after_unit" bind:value={generalForm.validate_after_unit} options={validateAfterUnits} />
      </div>
    </div>

    <div class="field-row">
      <Label forId="dataloader_threads">Dataloader Threads</Label>
      <Input type="number" min={0} name="dataloader_threads" bind:value={generalForm.dataloader_threads} />
    </div>

    <div class="field-row">
      <Label forId="train_device">Train Device</Label>
      <Input name="train_device" bind:value={generalForm.train_device} />
    </div>

    <div class="field-row switch-row">
      <Label forId="multi_gpu">Multi-GPU</Label>
      <Switch name="multi_gpu" bind:checked={generalForm.multi_gpu} />
    </div>

    <div class="field-row">
      <Label forId="device_indexes">Device Indexes</Label>
      <Input name="device_indexes" bind:value={generalForm.device_indexes} />
    </div>

    <div class="field-row">
      <Label forId="gradient_reduce_precision">Gradient Reduce Precision</Label>
      <Select
        name="gradient_reduce_precision"
        bind:value={generalForm.gradient_reduce_precision}
        options={gradientReducePrecisions}
      />
    </div>

    <div class="field-row switch-row">
      <Label forId="fused_gradient_reduce">Fused Gradient Reduce</Label>
      <Switch name="fused_gradient_reduce" bind:checked={generalForm.fused_gradient_reduce} />
    </div>

    <div class="field-row switch-row">
      <Label forId="async_gradient_reduce">Async Gradient Reduce</Label>
      <Switch name="async_gradient_reduce" bind:checked={generalForm.async_gradient_reduce} />
    </div>

    <div class="field-row">
      <Label forId="async_gradient_reduce_buffer">Buffer size (MB)</Label>
      <Input
        type="number"
        min={0}
        name="async_gradient_reduce_buffer"
        bind:value={generalForm.async_gradient_reduce_buffer}
      />
    </div>

    <div class="field-row">
      <Label forId="temp_device">Temp Device</Label>
      <Input name="temp_device" bind:value={generalForm.temp_device} />
    </div>
  </div>

  <div class="action-row">
    <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save General Settings'}</Button>
    <Button type="button" disabled={saving} on:click={onReload}>Reload</Button>
  </div>
</form>
