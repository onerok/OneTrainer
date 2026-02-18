<script lang="ts">
  import type { DataSettings } from '../../lib/api/types';
  import Button from '../../lib/components/ui/Button.svelte';
  import Label from '../../lib/components/ui/Label.svelte';
  import Switch from '../../lib/components/ui/Switch.svelte';

  export let dataForm: DataSettings;
  export let saving = false;
  export let onSubmit: (event: SubmitEvent) => void | Promise<void>;
  export let onReload: () => void | Promise<void>;
</script>

<form class="general-form" on:submit={onSubmit}>
  <div class="field-grid">
    <div class="field-row switch-row full-width">
      <Label forId="aspect_ratio_bucketing">Aspect Ratio Bucketing</Label>
      <Switch name="aspect_ratio_bucketing" bind:checked={dataForm.aspect_ratio_bucketing} />
    </div>

    <div class="field-row switch-row full-width">
      <Label forId="latent_caching">Latent Caching</Label>
      <Switch name="latent_caching" bind:checked={dataForm.latent_caching} />
    </div>

    <div class="field-row switch-row full-width">
      <Label forId="clear_cache_before_training">Clear cache before training</Label>
      <Switch name="clear_cache_before_training" bind:checked={dataForm.clear_cache_before_training} />
    </div>
  </div>

  <div class="action-row">
    <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save Data Settings'}</Button>
    <Button type="button" disabled={saving} on:click={onReload}>Reload</Button>
  </div>
</form>
