<script lang="ts">
  import type { TrainingSettings } from '../../lib/api/types';
  import Button from '../../lib/components/ui/Button.svelte';
  import Input from '../../lib/components/ui/Input.svelte';
  import Label from '../../lib/components/ui/Label.svelte';
  import Select from '../../lib/components/ui/Select.svelte';
  import Switch from '../../lib/components/ui/Switch.svelte';

  export let trainingForm: TrainingSettings;
  export let trainingClipGradNorm: number | '' = '';
  export let optimizers: string[] = [];
  export let learningRateSchedulers: string[] = [];
  export let learningRateScalers: string[] = [];
  export let emaModes: string[] = [];
  export let gradientCheckpointingMethods: string[] = [];
  export let trainDtypes: string[] = [];
  export let fallbackTrainDtypes: string[] = [];
  export let saving = false;
  export let onSubmit: (event: SubmitEvent) => void | Promise<void>;
  export let onReload: () => void | Promise<void>;
</script>

<form class="general-form" on:submit={onSubmit}>
  <div class="field-grid">
    <div class="field-row">
      <Label forId="optimizer">Optimizer</Label>
      <Select name="optimizer" bind:value={trainingForm.optimizer} options={optimizers} />
    </div>

    <div class="field-row">
      <Label forId="learning_rate_scheduler">Learning Rate Scheduler</Label>
      <Select
        name="learning_rate_scheduler"
        bind:value={trainingForm.learning_rate_scheduler}
        options={learningRateSchedulers}
      />
    </div>

    <div class="field-row">
      <Label forId="learning_rate">Learning Rate</Label>
      <Input type="number" min={0} step="any" name="learning_rate" bind:value={trainingForm.learning_rate} />
    </div>

    <div class="field-row">
      <Label forId="learning_rate_warmup_steps">Learning Rate Warmup Steps</Label>
      <Input
        type="number"
        min={0}
        step="any"
        name="learning_rate_warmup_steps"
        bind:value={trainingForm.learning_rate_warmup_steps}
      />
    </div>

    <div class="field-row">
      <Label forId="learning_rate_min_factor">Learning Rate Min Factor</Label>
      <Input
        type="number"
        min={0}
        step="any"
        name="learning_rate_min_factor"
        bind:value={trainingForm.learning_rate_min_factor}
      />
    </div>

    <div class="field-row">
      <Label forId="learning_rate_cycles">Learning Rate Cycles</Label>
      <Input
        type="number"
        min={0}
        step="any"
        name="learning_rate_cycles"
        bind:value={trainingForm.learning_rate_cycles}
      />
    </div>

    <div class="field-row">
      <Label forId="epochs">Epochs</Label>
      <Input type="number" min={1} name="epochs" bind:value={trainingForm.epochs} />
    </div>

    <div class="field-row">
      <Label forId="batch_size">Local Batch Size</Label>
      <Input type="number" min={1} name="batch_size" bind:value={trainingForm.batch_size} />
    </div>

    <div class="field-row">
      <Label forId="gradient_accumulation_steps">Accumulation Steps</Label>
      <Input
        type="number"
        min={1}
        name="gradient_accumulation_steps"
        bind:value={trainingForm.gradient_accumulation_steps}
      />
    </div>

    <div class="field-row">
      <Label forId="learning_rate_scaler">Learning Rate Scaler</Label>
      <Select
        name="learning_rate_scaler"
        bind:value={trainingForm.learning_rate_scaler}
        options={learningRateScalers}
      />
    </div>

    <div class="field-row">
      <Label forId="clip_grad_norm">Clip Grad Norm</Label>
      <Input type="number" min={0} step="any" name="clip_grad_norm" bind:value={trainingClipGradNorm} />
    </div>

    <div class="field-row">
      <Label forId="ema">EMA</Label>
      <Select name="ema" bind:value={trainingForm.ema} options={emaModes} />
    </div>

    <div class="field-row">
      <Label forId="ema_decay">EMA Decay</Label>
      <Input type="number" min={0} max={1} step="any" name="ema_decay" bind:value={trainingForm.ema_decay} />
    </div>

    <div class="field-row">
      <Label forId="ema_update_step_interval">EMA Update Step Interval</Label>
      <Input
        type="number"
        min={1}
        name="ema_update_step_interval"
        bind:value={trainingForm.ema_update_step_interval}
      />
    </div>

    <div class="field-row">
      <Label forId="gradient_checkpointing">Gradient checkpointing</Label>
      <Select
        name="gradient_checkpointing"
        bind:value={trainingForm.gradient_checkpointing}
        options={gradientCheckpointingMethods}
      />
    </div>

    <div class="field-row">
      <Label forId="layer_offload_fraction">Layer offload fraction</Label>
      <Input
        type="number"
        min={0}
        max={1}
        step="any"
        name="layer_offload_fraction"
        bind:value={trainingForm.layer_offload_fraction}
      />
    </div>

    <div class="field-row">
      <Label forId="train_dtype">Train Data Type</Label>
      <Select name="train_dtype" bind:value={trainingForm.train_dtype} options={trainDtypes} />
    </div>

    <div class="field-row">
      <Label forId="fallback_train_dtype">Fallback Train Data Type</Label>
      <Select
        name="fallback_train_dtype"
        bind:value={trainingForm.fallback_train_dtype}
        options={fallbackTrainDtypes}
      />
    </div>

    <div class="field-row switch-row">
      <Label forId="enable_autocast_cache">Autocast Cache</Label>
      <Switch name="enable_autocast_cache" bind:checked={trainingForm.enable_autocast_cache} />
    </div>

    <div class="field-row">
      <Label forId="resolution">Resolution</Label>
      <Input name="resolution" bind:value={trainingForm.resolution} />
    </div>

    <div class="field-row switch-row">
      <Label forId="force_circular_padding">Force Circular Padding</Label>
      <Switch name="force_circular_padding" bind:checked={trainingForm.force_circular_padding} />
    </div>
  </div>

  <div class="action-row">
    <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save Training Settings'}</Button>
    <Button type="button" disabled={saving} on:click={onReload}>Reload</Button>
  </div>
</form>
