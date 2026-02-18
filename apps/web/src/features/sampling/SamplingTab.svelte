<script lang="ts">
  import type { SamplingSettings } from '../../lib/api/types';
  import Button from '../../lib/components/ui/Button.svelte';
  import Input from '../../lib/components/ui/Input.svelte';
  import Label from '../../lib/components/ui/Label.svelte';
  import Select from '../../lib/components/ui/Select.svelte';
  import Switch from '../../lib/components/ui/Switch.svelte';

  export let samplingForm: SamplingSettings;
  export let sampleAfterUnits: string[] = [];
  export let sampleImageFormats: string[] = [];
  export let sampleVideoFormats: string[] = [];
  export let sampleAudioFormats: string[] = [];
  export let noiseSchedulers: string[] = [];
  export let saving = false;
  export let onSubmit: (event: SubmitEvent) => void | Promise<void>;
  export let onReload: () => void | Promise<void>;
  export let addSample: () => void;
  export let removeSample: (index: number) => void;
</script>

<form class="general-form" on:submit={onSubmit}>
  <div class="field-grid">
    <div class="field-row full-width">
      <Label forId="sample_definition_file_name">Sample Config File</Label>
      <Input name="sample_definition_file_name" bind:value={samplingForm.sample_definition_file_name} />
    </div>

    <div class="field-row split-row">
      <div>
        <Label forId="sample_after">Sample after</Label>
        <Input type="number" min={0} step="any" name="sample_after" bind:value={samplingForm.sample_after} />
      </div>
      <div>
        <Label forId="sample_after_unit">Unit</Label>
        <Select name="sample_after_unit" bind:value={samplingForm.sample_after_unit} options={sampleAfterUnits} />
      </div>
    </div>

    <div class="field-row">
      <Label forId="sample_skip_first">Sample skip first</Label>
      <Input type="number" min={0} name="sample_skip_first" bind:value={samplingForm.sample_skip_first} />
    </div>

    <div class="field-row">
      <Label forId="sample_image_format">Sample image format</Label>
      <Select name="sample_image_format" bind:value={samplingForm.sample_image_format} options={sampleImageFormats} />
    </div>

    <div class="field-row">
      <Label forId="sample_video_format">Sample video format</Label>
      <Select name="sample_video_format" bind:value={samplingForm.sample_video_format} options={sampleVideoFormats} />
    </div>

    <div class="field-row">
      <Label forId="sample_audio_format">Sample audio format</Label>
      <Select name="sample_audio_format" bind:value={samplingForm.sample_audio_format} options={sampleAudioFormats} />
    </div>

    <div class="field-row switch-row">
      <Label forId="samples_to_tensorboard">Samples to Tensorboard</Label>
      <Switch name="samples_to_tensorboard" bind:checked={samplingForm.samples_to_tensorboard} />
    </div>

    <div class="field-row switch-row">
      <Label forId="non_ema_sampling">Non-EMA Sampling</Label>
      <Switch name="non_ema_sampling" bind:checked={samplingForm.non_ema_sampling} />
    </div>

    <div class="field-row full-width">
      <Button type="button" disabled={saving} on:click={addSample}>Add Sample</Button>
    </div>

    {#each samplingForm.samples as sample, i}
      <div class="field-row full-width">
        <div class="concept-header">
          <strong>Sample {i + 1}</strong>
          <Button type="button" disabled={saving} on:click={() => removeSample(i)}>Remove</Button>
        </div>

        <div class="concept-grid">
          <div>
            <Label forId={`sample_width_${i}`}>Width</Label>
            <Input type="number" min={1} name={`sample_width_${i}`} bind:value={sample.width} />
          </div>
          <div>
            <Label forId={`sample_height_${i}`}>Height</Label>
            <Input type="number" min={1} name={`sample_height_${i}`} bind:value={sample.height} />
          </div>
          <div>
            <Label forId={`sample_seed_${i}`}>Seed</Label>
            <Input type="number" name={`sample_seed_${i}`} bind:value={sample.seed} />
          </div>
          <div>
            <Label forId={`sample_diffusion_steps_${i}`}>Diffusion Steps</Label>
            <Input type="number" min={1} name={`sample_diffusion_steps_${i}`} bind:value={sample.diffusion_steps} />
          </div>
          <div>
            <Label forId={`sample_cfg_scale_${i}`}>CFG Scale</Label>
            <Input type="number" min={0} step="any" name={`sample_cfg_scale_${i}`} bind:value={sample.cfg_scale} />
          </div>
          <div>
            <Label forId={`sample_noise_scheduler_${i}`}>Noise Scheduler</Label>
            <Select name={`sample_noise_scheduler_${i}`} bind:value={sample.noise_scheduler} options={noiseSchedulers} />
          </div>
          <div class="concept-full">
            <Label forId={`sample_prompt_${i}`}>Prompt</Label>
            <Input name={`sample_prompt_${i}`} bind:value={sample.prompt} />
          </div>
          <div class="concept-full">
            <Label forId={`sample_negative_prompt_${i}`}>Negative Prompt</Label>
            <Input name={`sample_negative_prompt_${i}`} bind:value={sample.negative_prompt} />
          </div>
          <div class="switch-inline">
            <Label forId={`sample_enabled_${i}`}>Enabled</Label>
            <Switch name={`sample_enabled_${i}`} bind:checked={sample.enabled} />
          </div>
          <div class="switch-inline">
            <Label forId={`sample_random_seed_${i}`}>Random Seed</Label>
            <Switch name={`sample_random_seed_${i}`} bind:checked={sample.random_seed} />
          </div>
        </div>
      </div>
    {/each}
  </div>

  <div class="action-row">
    <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save Sampling Settings'}</Button>
    <Button type="button" disabled={saving} on:click={onReload}>Reload</Button>
  </div>
</form>
