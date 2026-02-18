<script lang="ts">
  import type { LoraSettings } from '../../lib/api/types';
  import Button from '../../lib/components/ui/Button.svelte';
  import Input from '../../lib/components/ui/Input.svelte';
  import Label from '../../lib/components/ui/Label.svelte';
  import Select from '../../lib/components/ui/Select.svelte';
  import Switch from '../../lib/components/ui/Switch.svelte';

  export let loraForm: LoraSettings;
  export let peftTypes: string[] = [];
  export let loraWeightDtypes: string[] = [];
  export let saving = false;
  export let onSubmit: (event: SubmitEvent) => void | Promise<void>;
  export let onReload: () => void | Promise<void>;
</script>

<form class="general-form" on:submit={onSubmit}>
  <div class="field-grid">
    <div class="field-row">
      <Label forId="peft_type">Type</Label>
      <Select name="peft_type" bind:value={loraForm.peft_type} options={peftTypes} />
    </div>

    <div class="field-row full-width">
      <Label forId="lora_model_name">Base Model</Label>
      <Input name="lora_model_name" bind:value={loraForm.lora_model_name} />
    </div>

    {#if loraForm.peft_type === 'LORA' || loraForm.peft_type === 'LOHA'}
      <div class="field-row">
        <Label forId="lora_rank">Rank</Label>
        <Input type="number" min={1} name="lora_rank" bind:value={loraForm.lora_rank} />
      </div>

      <div class="field-row">
        <Label forId="lora_alpha">Alpha</Label>
        <Input type="number" min={0} step="any" name="lora_alpha" bind:value={loraForm.lora_alpha} />
      </div>

      <div class="field-row">
        <Label forId="dropout_probability">Dropout Probability</Label>
        <Input
          type="number"
          min={0}
          max={1}
          step="any"
          name="dropout_probability"
          bind:value={loraForm.dropout_probability}
        />
      </div>

      <div class="field-row">
        <Label forId="lora_weight_dtype">Weight Data Type</Label>
        <Select name="lora_weight_dtype" bind:value={loraForm.lora_weight_dtype} options={loraWeightDtypes} />
      </div>

      <div class="field-row switch-row">
        <Label forId="bundle_additional_embeddings">Bundle Embeddings</Label>
        <Switch
          name="bundle_additional_embeddings"
          bind:checked={loraForm.bundle_additional_embeddings}
        />
      </div>
    {/if}

    {#if loraForm.peft_type === 'LORA'}
      <div class="field-row switch-row">
        <Label forId="lora_decompose">Decompose Weights (DoRA)</Label>
        <Switch name="lora_decompose" bind:checked={loraForm.lora_decompose} />
      </div>

      <div class="field-row switch-row">
        <Label forId="lora_decompose_norm_epsilon">Use Norm Epsilon</Label>
        <Switch
          name="lora_decompose_norm_epsilon"
          bind:checked={loraForm.lora_decompose_norm_epsilon}
        />
      </div>

      <div class="field-row switch-row">
        <Label forId="lora_decompose_output_axis">Apply on output axis</Label>
        <Switch
          name="lora_decompose_output_axis"
          bind:checked={loraForm.lora_decompose_output_axis}
        />
      </div>
    {/if}

    {#if loraForm.peft_type === 'OFT_2'}
      <div class="field-row">
        <Label forId="oft_block_size">OFT Block Size</Label>
        <Input type="number" min={1} name="oft_block_size" bind:value={loraForm.oft_block_size} />
      </div>

      <div class="field-row switch-row">
        <Label forId="oft_coft">Constrained OFT (COFT)</Label>
        <Switch name="oft_coft" bind:checked={loraForm.oft_coft} />
      </div>

      <div class="field-row">
        <Label forId="coft_eps">COFT Epsilon</Label>
        <Input type="number" min={0} step="any" name="coft_eps" bind:value={loraForm.coft_eps} />
      </div>

      <div class="field-row switch-row">
        <Label forId="oft_block_share">Block Share</Label>
        <Switch name="oft_block_share" bind:checked={loraForm.oft_block_share} />
      </div>

      <div class="field-row">
        <Label forId="dropout_probability_oft">Dropout Probability</Label>
        <Input
          type="number"
          min={0}
          max={1}
          step="any"
          name="dropout_probability_oft"
          bind:value={loraForm.dropout_probability}
        />
      </div>

      <div class="field-row">
        <Label forId="lora_weight_dtype_oft">OFT Weight Data Type</Label>
        <Select
          name="lora_weight_dtype_oft"
          bind:value={loraForm.lora_weight_dtype}
          options={loraWeightDtypes}
        />
      </div>

      <div class="field-row switch-row">
        <Label forId="bundle_additional_embeddings_oft">Bundle Embeddings</Label>
        <Switch
          name="bundle_additional_embeddings_oft"
          bind:checked={loraForm.bundle_additional_embeddings}
        />
      </div>
    {/if}
  </div>

  <div class="action-row">
    <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save LoRA Settings'}</Button>
    <Button type="button" disabled={saving} on:click={onReload}>Reload</Button>
  </div>
</form>
