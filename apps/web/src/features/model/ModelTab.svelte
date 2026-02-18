<script lang="ts">
  import type { ModelSettings } from '../../lib/api/types';
  import Button from '../../lib/components/ui/Button.svelte';
  import Input from '../../lib/components/ui/Input.svelte';
  import Label from '../../lib/components/ui/Label.svelte';
  import Select from '../../lib/components/ui/Select.svelte';
  import Switch from '../../lib/components/ui/Switch.svelte';

  export let modelForm: ModelSettings;
  export let trainingMethods: string[] = [];
  export let modelTypes: string[] = [];
  export let dataTypes: string[] = [];
  export let outputDtypes: string[] = [];
  export let modelFormats: string[] = [];
  export let includeTrainConfigs: string[] = [];
  export let quantizationPresets: string[] = [];
  export let saving = false;
  export let onSubmit: (event: SubmitEvent) => void | Promise<void>;
  export let onReload: () => void | Promise<void>;
</script>

<form class="general-form" on:submit={onSubmit}>
  <div class="field-grid">
    <div class="field-row">
      <Label forId="training_method">Training Method</Label>
      <Select name="training_method" bind:value={modelForm.training_method} options={trainingMethods} />
    </div>

    <div class="field-row">
      <Label forId="model_type">Model Type</Label>
      <Select name="model_type" bind:value={modelForm.model_type} options={modelTypes} />
    </div>

    <div class="field-row full-width">
      <Label forId="huggingface_token">Hugging Face Token</Label>
      <Input name="huggingface_token" bind:value={modelForm.huggingface_token} />
    </div>

    <div class="field-row full-width">
      <Label forId="base_model_name">Base Model</Label>
      <Input name="base_model_name" bind:value={modelForm.base_model_name} />
    </div>

    <div class="field-row switch-row">
      <Label forId="compile">Compile transformer blocks</Label>
      <Switch name="compile" bind:checked={modelForm.compile} />
    </div>

    <div class="field-row">
      <Label forId="unet_weight_dtype">UNet Data Type</Label>
      <Select name="unet_weight_dtype" bind:value={modelForm.unet.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="prior_model_name">Prior Model</Label>
      <Input name="prior_model_name" bind:value={modelForm.prior.model_name} />
    </div>

    <div class="field-row">
      <Label forId="prior_weight_dtype">Prior Data Type</Label>
      <Select name="prior_weight_dtype" bind:value={modelForm.prior.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="transformer_model_name">Override Transformer / GGUF</Label>
      <Input name="transformer_model_name" bind:value={modelForm.transformer.model_name} />
    </div>

    <div class="field-row">
      <Label forId="transformer_weight_dtype">Transformer Data Type</Label>
      <Select name="transformer_weight_dtype" bind:value={modelForm.transformer.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="text_encoder_weight_dtype">Text Encoder Data Type</Label>
      <Select name="text_encoder_weight_dtype" bind:value={modelForm.text_encoder.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="text_encoder_2_weight_dtype">Text Encoder 2 Data Type</Label>
      <Select name="text_encoder_2_weight_dtype" bind:value={modelForm.text_encoder_2.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="text_encoder_3_weight_dtype">Text Encoder 3 Data Type</Label>
      <Select name="text_encoder_3_weight_dtype" bind:value={modelForm.text_encoder_3.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="text_encoder_4_model_name">Text Encoder 4 Override</Label>
      <Input name="text_encoder_4_model_name" bind:value={modelForm.text_encoder_4.model_name} />
    </div>

    <div class="field-row">
      <Label forId="text_encoder_4_weight_dtype">Text Encoder 4 Data Type</Label>
      <Select name="text_encoder_4_weight_dtype" bind:value={modelForm.text_encoder_4.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="vae_model_name">VAE Override</Label>
      <Input name="vae_model_name" bind:value={modelForm.vae.model_name} />
    </div>

    <div class="field-row">
      <Label forId="vae_weight_dtype">VAE Data Type</Label>
      <Select name="vae_weight_dtype" bind:value={modelForm.vae.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="effnet_encoder_model_name">Effnet Encoder Model</Label>
      <Input name="effnet_encoder_model_name" bind:value={modelForm.effnet_encoder.model_name} />
    </div>

    <div class="field-row">
      <Label forId="effnet_encoder_weight_dtype">Effnet Encoder Data Type</Label>
      <Select name="effnet_encoder_weight_dtype" bind:value={modelForm.effnet_encoder.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="decoder_model_name">Decoder Model</Label>
      <Input name="decoder_model_name" bind:value={modelForm.decoder.model_name} />
    </div>

    <div class="field-row">
      <Label forId="decoder_weight_dtype">Decoder Data Type</Label>
      <Select name="decoder_weight_dtype" bind:value={modelForm.decoder.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="decoder_text_encoder_weight_dtype">Decoder Text Encoder Data Type</Label>
      <Select name="decoder_text_encoder_weight_dtype" bind:value={modelForm.decoder_text_encoder.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="decoder_vqgan_weight_dtype">Decoder VQGAN Data Type</Label>
      <Select name="decoder_vqgan_weight_dtype" bind:value={modelForm.decoder_vqgan.weight_dtype} options={dataTypes} />
    </div>

    <div class="field-row">
      <Label forId="quantization_layer_filter_preset">Quantization Layer Filter Preset</Label>
      <Select name="quantization_layer_filter_preset" bind:value={modelForm.quantization.layer_filter_preset} options={quantizationPresets} />
    </div>

    <div class="field-row">
      <Label forId="quantization_svd_dtype">SVDQuant Data Type</Label>
      <Select name="quantization_svd_dtype" bind:value={modelForm.quantization.svd_dtype} options={dataTypes} />
    </div>

    <div class="field-row full-width">
      <Label forId="quantization_layer_filter">Quantization Layer Filter</Label>
      <Input name="quantization_layer_filter" bind:value={modelForm.quantization.layer_filter} />
    </div>

    <div class="field-row switch-row">
      <Label forId="quantization_layer_filter_regex">Quantization Layer Filter Regex</Label>
      <Switch name="quantization_layer_filter_regex" bind:checked={modelForm.quantization.layer_filter_regex} />
    </div>

    <div class="field-row">
      <Label forId="quantization_svd_rank">SVDQuant Rank</Label>
      <Input type="number" min={1} name="quantization_svd_rank" bind:value={modelForm.quantization.svd_rank} />
    </div>

    <div class="field-row full-width">
      <Label forId="output_model_destination">Model Output Destination</Label>
      <Input name="output_model_destination" bind:value={modelForm.output_model_destination} />
    </div>

    <div class="field-row">
      <Label forId="output_dtype">Output Data Type</Label>
      <Select name="output_dtype" bind:value={modelForm.output_dtype} options={outputDtypes} />
    </div>

    <div class="field-row">
      <Label forId="output_model_format">Output Format</Label>
      <Select name="output_model_format" bind:value={modelForm.output_model_format} options={modelFormats} />
    </div>

    <div class="field-row">
      <Label forId="include_train_config">Include Config</Label>
      <Select name="include_train_config" bind:value={modelForm.include_train_config} options={includeTrainConfigs} />
    </div>
  </div>

  <div class="action-row">
    <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save Model Settings'}</Button>
    <Button type="button" disabled={saving} on:click={onReload}>Reload</Button>
  </div>
</form>
