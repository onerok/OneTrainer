<script lang="ts">
  import { onMount } from 'svelte';
  import {
    fetchBackupConfig,
    fetchConceptsConfig,
    fetchDataConfig,
    fetchGeneralConfig,
    fetchLoraConfig,
    fetchModelConfig,
    fetchSamplingConfig,
    fetchTrainingConfig,
    fetchToolsConfig,
    saveBackupConfig,
    saveConceptsConfig,
    saveDataConfig,
    saveGeneralConfig,
    saveLoraConfig,
    saveModelConfig,
    saveSamplingConfig,
    saveTrainingConfig
  } from '../lib/api/client';
  import type {
    BackupSettings,
    BalancingStrategyValue,
    ConceptSettings,
    ConceptsSettings,
    DataSettings,
    GeneralSettings,
    LoraSettings,
    ModelSettings,
    SamplingSampleSettings,
    SamplingSettings,
    ToolInfo,
    TrainingSettings
  } from '../lib/api/types';
  import Button from '../lib/components/ui/Button.svelte';
  import Card from '../lib/components/ui/Card.svelte';
  import Input from '../lib/components/ui/Input.svelte';
  import Label from '../lib/components/ui/Label.svelte';
  import Select from '../lib/components/ui/Select.svelte';
  import Switch from '../lib/components/ui/Switch.svelte';
  import Tabs from '../lib/components/ui/Tabs.svelte';
  import BackupTab from '../features/backup/BackupTab.svelte';
  import DataTab from '../features/data/DataTab.svelte';
  import LoraTab from '../features/lora/LoraTab.svelte';
  import TrainingTab from '../features/training/TrainingTab.svelte';
  import ToolsTab from '../features/tools/ToolsTab.svelte';

  let activeTab = 'general';

  let generalForm: GeneralSettings | null = null;
  let validateAfterUnits: string[] = [];
  let gradientReducePrecisions: string[] = [];

  let modelForm: ModelSettings | null = null;
  let trainingMethods: string[] = [];
  let modelTypes: string[] = [];
  let dataTypes: string[] = [];
  let outputDtypes: string[] = [];
  let modelFormats: string[] = [];
  let includeTrainConfigs: string[] = [];
  let quantizationPresets: string[] = [];

  let loraForm: LoraSettings | null = null;
  let peftTypes: string[] = [];
  let loraWeightDtypes: string[] = [];

  let dataForm: DataSettings | null = null;

  let backupForm: BackupSettings | null = null;
  let backupAfterUnits: string[] = [];
  let saveEveryUnits: string[] = [];

  let samplingForm: SamplingSettings | null = null;
  let sampleAfterUnits: string[] = [];
  let sampleImageFormats: string[] = [];
  let sampleVideoFormats: string[] = [];
  let sampleAudioFormats: string[] = [];
  let noiseSchedulers: string[] = [];

  let trainingForm: TrainingSettings | null = null;
  let trainingClipGradNorm: number | '' = '';
  let optimizers: string[] = [];
  let learningRateSchedulers: string[] = [];
  let learningRateScalers: string[] = [];
  let emaModes: string[] = [];
  let gradientCheckpointingMethods: string[] = [];
  let trainDtypes: string[] = [];
  let fallbackTrainDtypes: string[] = [];
  let toolsList: ToolInfo[] = [];

  let conceptsForm: ConceptsSettings | null = null;
  let conceptTypes: string[] = [];
  let balancingStrategies: string[] = [];
  let promptSources: string[] = [];

  let loading = true;
  let saving = false;
  let statusMessage = '';
  let errorMessage = '';

  onMount(async () => {
    await loadGeneralConfig();
    await loadModelConfig();
    await loadLoraConfig();
    await loadDataConfig();
    await loadBackupConfig();
    await loadSamplingConfig();
    await loadTrainingConfig();
    await loadToolsConfig();
    await loadConceptsConfig();
  });

  async function loadGeneralConfig() {
    loading = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await fetchGeneralConfig();
      generalForm = response.data;
      validateAfterUnits = response.meta.validate_after_units;
      gradientReducePrecisions = response.meta.gradient_reduce_precisions;
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to load General config';
    } finally {
      loading = false;
    }
  }

  async function loadModelConfig() {
    loading = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await fetchModelConfig();
      modelForm = response.data;
      trainingMethods = response.meta.training_methods;
      modelTypes = response.meta.model_types;
      dataTypes = response.meta.data_types;
      outputDtypes = response.meta.output_dtypes;
      modelFormats = response.meta.model_formats;
      includeTrainConfigs = response.meta.include_train_configs;
      quantizationPresets = response.meta.quantization_presets;
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to load Model config';
    } finally {
      loading = false;
    }
  }

  async function loadDataConfig() {
    loading = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await fetchDataConfig();
      dataForm = response.data;
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to load Data config';
    } finally {
      loading = false;
    }
  }

  async function loadLoraConfig() {
    loading = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await fetchLoraConfig();
      loraForm = response.data;
      peftTypes = response.meta.peft_types;
      loraWeightDtypes = response.meta.lora_weight_dtypes;
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to load LoRA config';
    } finally {
      loading = false;
    }
  }

  async function loadConceptsConfig() {
    loading = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await fetchConceptsConfig();
      conceptsForm = response.data;
      conceptTypes = response.meta.concept_types;
      balancingStrategies = response.meta.balancing_strategies;
      promptSources = response.meta.prompt_sources;
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to load Concepts config';
    } finally {
      loading = false;
    }
  }

  async function loadBackupConfig() {
    loading = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await fetchBackupConfig();
      backupForm = response.data;
      backupAfterUnits = response.meta.backup_after_units;
      saveEveryUnits = response.meta.save_every_units;
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to load Backup config';
    } finally {
      loading = false;
    }
  }

  async function loadSamplingConfig() {
    loading = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await fetchSamplingConfig();
      samplingForm = response.data;
      sampleAfterUnits = response.meta.sample_after_units;
      sampleImageFormats = response.meta.sample_image_formats;
      sampleVideoFormats = response.meta.sample_video_formats;
      sampleAudioFormats = response.meta.sample_audio_formats;
      noiseSchedulers = response.meta.noise_schedulers;
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to load Sampling config';
    } finally {
      loading = false;
    }
  }

  async function loadTrainingConfig() {
    loading = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await fetchTrainingConfig();
      trainingForm = response.data;
      trainingClipGradNorm = response.data.clip_grad_norm ?? '';
      optimizers = response.meta.optimizers;
      learningRateSchedulers = response.meta.learning_rate_schedulers;
      learningRateScalers = response.meta.learning_rate_scalers;
      emaModes = response.meta.ema_modes;
      gradientCheckpointingMethods = response.meta.gradient_checkpointing_methods;
      trainDtypes = response.meta.train_dtypes;
      fallbackTrainDtypes = response.meta.fallback_train_dtypes;
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to load Training config';
    } finally {
      loading = false;
    }
  }

  async function loadToolsConfig() {
    loading = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await fetchToolsConfig();
      toolsList = response.data.tools;
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to load Tools config';
    } finally {
      loading = false;
    }
  }

  async function onSubmitGeneral(event: SubmitEvent) {
    event.preventDefault();
    if (!generalForm) {
      return;
    }

    saving = true;
    errorMessage = '';
    statusMessage = '';

    const payload: GeneralSettings = {
      ...generalForm,
      tensorboard_port: Number(generalForm.tensorboard_port),
      validate_after: Number(generalForm.validate_after),
      dataloader_threads: Number(generalForm.dataloader_threads),
      async_gradient_reduce_buffer: Number(generalForm.async_gradient_reduce_buffer)
    };

    try {
      const response = await saveGeneralConfig(payload);
      generalForm = response.data;
      statusMessage = 'General settings saved.';
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to save General config';
    } finally {
      saving = false;
    }
  }

  async function onSubmitModel(event: SubmitEvent) {
    event.preventDefault();
    if (!modelForm) {
      return;
    }

    saving = true;
    errorMessage = '';
    statusMessage = '';

    const payload: ModelSettings = {
      ...modelForm,
      quantization: {
        ...modelForm.quantization,
        svd_rank: Number(modelForm.quantization.svd_rank)
      }
    };

    try {
      const response = await saveModelConfig(payload);
      modelForm = response.data;
      statusMessage = 'Model settings saved.';
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to save Model config';
    } finally {
      saving = false;
    }
  }

  async function onSubmitData(event: SubmitEvent) {
    event.preventDefault();
    if (!dataForm) {
      return;
    }

    saving = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await saveDataConfig(dataForm);
      dataForm = response.data;
      statusMessage = 'Data settings saved.';
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to save Data config';
    } finally {
      saving = false;
    }
  }

  async function onSubmitLora(event: SubmitEvent) {
    event.preventDefault();
    if (!loraForm) {
      return;
    }

    saving = true;
    errorMessage = '';
    statusMessage = '';

    const payload: LoraSettings = {
      ...loraForm,
      lora_rank: Number(loraForm.lora_rank),
      lora_alpha: Number(loraForm.lora_alpha),
      dropout_probability: Number(loraForm.dropout_probability),
      oft_block_size: Number(loraForm.oft_block_size),
      coft_eps: Number(loraForm.coft_eps)
    };

    try {
      const response = await saveLoraConfig(payload);
      loraForm = response.data;
      statusMessage = 'LoRA settings saved.';
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to save LoRA config';
    } finally {
      saving = false;
    }
  }

  async function onSubmitConcepts(event: SubmitEvent) {
    event.preventDefault();
    if (!conceptsForm) {
      return;
    }

    saving = true;
    errorMessage = '';
    statusMessage = '';

    try {
      const response = await saveConceptsConfig(conceptsForm);
      conceptsForm = response.data;
      statusMessage = 'Concept settings saved.';
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to save Concepts config';
    } finally {
      saving = false;
    }
  }

  async function onSubmitBackup(event: SubmitEvent) {
    event.preventDefault();
    if (!backupForm) {
      return;
    }

    saving = true;
    errorMessage = '';
    statusMessage = '';

    const payload: BackupSettings = {
      ...backupForm,
      backup_after: Number(backupForm.backup_after),
      rolling_backup_count: Number(backupForm.rolling_backup_count),
      save_every: Number(backupForm.save_every),
      save_skip_first: Number(backupForm.save_skip_first)
    };

    try {
      const response = await saveBackupConfig(payload);
      backupForm = response.data;
      statusMessage = 'Backup settings saved.';
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to save Backup config';
    } finally {
      saving = false;
    }
  }

  async function onSubmitSampling(event: SubmitEvent) {
    event.preventDefault();
    if (!samplingForm) {
      return;
    }

    saving = true;
    errorMessage = '';
    statusMessage = '';

    const payload: SamplingSettings = {
      ...samplingForm,
      sample_after: Number(samplingForm.sample_after),
      sample_skip_first: Number(samplingForm.sample_skip_first),
      samples: samplingForm.samples.map((sample) => ({
        ...sample,
        width: Number(sample.width),
        height: Number(sample.height),
        frames: Number(sample.frames),
        length: Number(sample.length),
        seed: Number(sample.seed),
        diffusion_steps: Number(sample.diffusion_steps),
        cfg_scale: Number(sample.cfg_scale),
        text_encoder_1_layer_skip: Number(sample.text_encoder_1_layer_skip),
        text_encoder_1_sequence_length:
          sample.text_encoder_1_sequence_length === null || sample.text_encoder_1_sequence_length === undefined
            ? null
            : Number(sample.text_encoder_1_sequence_length),
        text_encoder_2_layer_skip: Number(sample.text_encoder_2_layer_skip),
        text_encoder_2_sequence_length:
          sample.text_encoder_2_sequence_length === null || sample.text_encoder_2_sequence_length === undefined
            ? null
            : Number(sample.text_encoder_2_sequence_length),
        text_encoder_3_layer_skip: Number(sample.text_encoder_3_layer_skip),
        text_encoder_4_layer_skip: Number(sample.text_encoder_4_layer_skip)
      }))
    };

    try {
      const response = await saveSamplingConfig(payload);
      samplingForm = response.data;
      statusMessage = 'Sampling settings saved.';
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to save Sampling config';
    } finally {
      saving = false;
    }
  }

  async function onSubmitTraining(event: SubmitEvent) {
    event.preventDefault();
    if (!trainingForm) {
      return;
    }

    saving = true;
    errorMessage = '';
    statusMessage = '';

    const payload: TrainingSettings = {
      ...trainingForm,
      learning_rate: Number(trainingForm.learning_rate),
      learning_rate_warmup_steps: Number(trainingForm.learning_rate_warmup_steps),
      learning_rate_min_factor: Number(trainingForm.learning_rate_min_factor),
      learning_rate_cycles: Number(trainingForm.learning_rate_cycles),
      epochs: Number(trainingForm.epochs),
      batch_size: Number(trainingForm.batch_size),
      gradient_accumulation_steps: Number(trainingForm.gradient_accumulation_steps),
      clip_grad_norm: trainingClipGradNorm === '' ? null : Number(trainingClipGradNorm),
      ema_decay: Number(trainingForm.ema_decay),
      ema_update_step_interval: Number(trainingForm.ema_update_step_interval),
      layer_offload_fraction: Number(trainingForm.layer_offload_fraction)
    };

    try {
      const response = await saveTrainingConfig(payload);
      trainingForm = response.data;
      trainingClipGradNorm = response.data.clip_grad_norm ?? '';
      statusMessage = 'Training settings saved.';
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Failed to save Training config';
    } finally {
      saving = false;
    }
  }

  function createDefaultConcept(): ConceptSettings {
    return {
      name: '',
      path: '',
      enabled: true,
      type: 'STANDARD',
      include_subdirectories: false,
      image_variations: 1,
      text_variations: 1,
      balancing: 1,
      balancing_strategy: 'REPEATS' as BalancingStrategyValue,
      loss_weight: 1,
      text: {
        prompt_source: 'sample',
        prompt_path: ''
      }
    };
  }

  function addConcept() {
    if (!conceptsForm) {
      return;
    }
    conceptsForm = {
      ...conceptsForm,
      concepts: [...conceptsForm.concepts, createDefaultConcept()]
    };
  }

  function removeConcept(index: number) {
    if (!conceptsForm) {
      return;
    }
    conceptsForm = {
      ...conceptsForm,
      concepts: conceptsForm.concepts.filter((_, i) => i !== index)
    };
  }

  function createDefaultSample(): SamplingSampleSettings {
    return {
      enabled: true,
      prompt: '',
      negative_prompt: '',
      height: 512,
      width: 512,
      frames: 1,
      length: 10,
      seed: 42,
      random_seed: false,
      diffusion_steps: 20,
      cfg_scale: 7,
      noise_scheduler: 'DDIM',
      text_encoder_1_layer_skip: 0,
      text_encoder_1_sequence_length: null,
      text_encoder_2_layer_skip: 0,
      text_encoder_2_sequence_length: null,
      text_encoder_3_layer_skip: 0,
      text_encoder_4_layer_skip: 0,
      transformer_attention_mask: false,
      force_last_timestep: false,
      sample_inpainting: false,
      base_image_path: '',
      mask_image_path: ''
    };
  }

  function addSample() {
    if (!samplingForm) {
      return;
    }
    samplingForm = {
      ...samplingForm,
      samples: [...samplingForm.samples, createDefaultSample()]
    };
  }

  function removeSample(index: number) {
    if (!samplingForm) {
      return;
    }
    samplingForm = {
      ...samplingForm,
      samples: samplingForm.samples.filter((_, i) => i !== index)
    };
  }

  function onTabChange(event: CustomEvent<{ tabId: string }>) {
    activeTab = event.detail.tabId;
    statusMessage = '';
    errorMessage = '';
  }

  async function onToolAction(tool: ToolInfo) {
    if (tool.action_type === 'WEB_LINK') {
      window.open(tool.action_value, '_blank', 'noopener,noreferrer');
      statusMessage = `${tool.name} opened.`;
      return;
    }

    if (tool.action_type === 'CLI_COMMAND') {
      try {
        await navigator.clipboard.writeText(tool.action_value);
        statusMessage = `${tool.name} command copied: ${tool.action_value}`;
      } catch {
        statusMessage = `${tool.name} command: ${tool.action_value}`;
      }
      return;
    }

    statusMessage = tool.action_value;
  }
</script>

<main class="page-shell">
  <section class="hero">
    <h1>OneTrainer Web UI</h1>
    <p>FastAPI backend + Svelte frontend. General, Model, LoRA, Data, Training, Sampling, Backup, Tools, and Concepts tabs are implemented.</p>
  </section>

  <Tabs activeTab={activeTab} on:change={onTabChange} />

  <Card>
    {#if loading}
      <p class="muted">
        Loading {activeTab === 'general'
          ? 'General'
          : activeTab === 'model'
            ? 'Model'
            : activeTab === 'lora'
              ? 'LoRA'
            : activeTab === 'data'
              ? 'Data'
              : activeTab === 'backup'
                ? 'Backup'
              : activeTab === 'sampling'
                ? 'Sampling'
              : activeTab === 'training'
                ? 'Training'
              : activeTab === 'tools'
                ? 'Tools'
                : 'Concepts'} settings...
      </p>
    {:else if activeTab === 'general' && !generalForm}
      <p class="error">Unable to initialize General settings.</p>
    {:else if activeTab === 'model' && !modelForm}
      <p class="error">Unable to initialize Model settings.</p>
    {:else if activeTab === 'lora' && !loraForm}
      <p class="error">Unable to initialize LoRA settings.</p>
    {:else if activeTab === 'data' && !dataForm}
      <p class="error">Unable to initialize Data settings.</p>
    {:else if activeTab === 'backup' && !backupForm}
      <p class="error">Unable to initialize Backup settings.</p>
    {:else if activeTab === 'sampling' && !samplingForm}
      <p class="error">Unable to initialize Sampling settings.</p>
    {:else if activeTab === 'training' && !trainingForm}
      <p class="error">Unable to initialize Training settings.</p>
    {:else if activeTab === 'tools' && toolsList.length === 0}
      <p class="error">Unable to initialize Tools settings.</p>
    {:else if activeTab === 'concepts' && !conceptsForm}
      <p class="error">Unable to initialize Concepts settings.</p>
    {:else if activeTab === 'general' && generalForm}
      <form class="general-form" on:submit={onSubmitGeneral}>
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
          <Button type="button" disabled={saving} on:click={loadGeneralConfig}>Reload</Button>
        </div>
      </form>
    {:else if activeTab === 'model' && modelForm}
      <form class="general-form" on:submit={onSubmitModel}>
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
            <Select
              name="text_encoder_weight_dtype"
              bind:value={modelForm.text_encoder.weight_dtype}
              options={dataTypes}
            />
          </div>

          <div class="field-row">
            <Label forId="text_encoder_2_weight_dtype">Text Encoder 2 Data Type</Label>
            <Select
              name="text_encoder_2_weight_dtype"
              bind:value={modelForm.text_encoder_2.weight_dtype}
              options={dataTypes}
            />
          </div>

          <div class="field-row">
            <Label forId="text_encoder_3_weight_dtype">Text Encoder 3 Data Type</Label>
            <Select
              name="text_encoder_3_weight_dtype"
              bind:value={modelForm.text_encoder_3.weight_dtype}
              options={dataTypes}
            />
          </div>

          <div class="field-row">
            <Label forId="text_encoder_4_model_name">Text Encoder 4 Override</Label>
            <Input name="text_encoder_4_model_name" bind:value={modelForm.text_encoder_4.model_name} />
          </div>

          <div class="field-row">
            <Label forId="text_encoder_4_weight_dtype">Text Encoder 4 Data Type</Label>
            <Select
              name="text_encoder_4_weight_dtype"
              bind:value={modelForm.text_encoder_4.weight_dtype}
              options={dataTypes}
            />
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
            <Select
              name="effnet_encoder_weight_dtype"
              bind:value={modelForm.effnet_encoder.weight_dtype}
              options={dataTypes}
            />
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
            <Select
              name="decoder_text_encoder_weight_dtype"
              bind:value={modelForm.decoder_text_encoder.weight_dtype}
              options={dataTypes}
            />
          </div>

          <div class="field-row">
            <Label forId="decoder_vqgan_weight_dtype">Decoder VQGAN Data Type</Label>
            <Select
              name="decoder_vqgan_weight_dtype"
              bind:value={modelForm.decoder_vqgan.weight_dtype}
              options={dataTypes}
            />
          </div>

          <div class="field-row">
            <Label forId="quantization_layer_filter_preset">Quantization Layer Filter Preset</Label>
            <Select
              name="quantization_layer_filter_preset"
              bind:value={modelForm.quantization.layer_filter_preset}
              options={quantizationPresets}
            />
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
            <Switch
              name="quantization_layer_filter_regex"
              bind:checked={modelForm.quantization.layer_filter_regex}
            />
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
            <Select
              name="include_train_config"
              bind:value={modelForm.include_train_config}
              options={includeTrainConfigs}
            />
          </div>
        </div>

        <div class="action-row">
          <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save Model Settings'}</Button>
          <Button type="button" disabled={saving} on:click={loadModelConfig}>Reload</Button>
        </div>
      </form>
    {:else if activeTab === 'lora' && loraForm}
      <LoraTab
        {loraForm}
        {peftTypes}
        {loraWeightDtypes}
        {saving}
        onSubmit={onSubmitLora}
        onReload={loadLoraConfig}
      />
    {:else if activeTab === 'data' && dataForm}
      <DataTab {dataForm} {saving} onSubmit={onSubmitData} onReload={loadDataConfig} />
    {:else if activeTab === 'sampling' && samplingForm}
      <form class="general-form" on:submit={onSubmitSampling}>
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
                  <Input
                    type="number"
                    min={1}
                    name={`sample_diffusion_steps_${i}`}
                    bind:value={sample.diffusion_steps}
                  />
                </div>
                <div>
                  <Label forId={`sample_cfg_scale_${i}`}>CFG Scale</Label>
                  <Input type="number" min={0} step="any" name={`sample_cfg_scale_${i}`} bind:value={sample.cfg_scale} />
                </div>
                <div>
                  <Label forId={`sample_noise_scheduler_${i}`}>Noise Scheduler</Label>
                  <Select
                    name={`sample_noise_scheduler_${i}`}
                    bind:value={sample.noise_scheduler}
                    options={noiseSchedulers}
                  />
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
          <Button type="button" disabled={saving} on:click={loadSamplingConfig}>Reload</Button>
        </div>
      </form>
    {:else if activeTab === 'backup' && backupForm}
      <BackupTab
        {backupForm}
        {backupAfterUnits}
        {saveEveryUnits}
        {saving}
        onSubmit={onSubmitBackup}
        onReload={loadBackupConfig}
      />
    {:else if activeTab === 'tools'}
      <ToolsTab {toolsList} {saving} onReload={loadToolsConfig} {onToolAction} />
    {:else if activeTab === 'training' && trainingForm}
      <TrainingTab
        {trainingForm}
        bind:trainingClipGradNorm
        {optimizers}
        {learningRateSchedulers}
        {learningRateScalers}
        {emaModes}
        {gradientCheckpointingMethods}
        {trainDtypes}
        {fallbackTrainDtypes}
        {saving}
        onSubmit={onSubmitTraining}
        onReload={loadTrainingConfig}
      />
    {:else if activeTab === 'concepts' && conceptsForm}
      <form class="general-form" on:submit={onSubmitConcepts}>
        <div class="field-grid">
          <div class="field-row full-width">
            <Label forId="concept_file_name">Concept Config File</Label>
            <Input name="concept_file_name" bind:value={conceptsForm.concept_file_name} />
          </div>

          <div class="field-row full-width">
            <Button type="button" disabled={saving} on:click={addConcept}>Add Concept</Button>
          </div>

          {#each conceptsForm.concepts as concept, i}
            <div class="field-row full-width">
              <div class="concept-header">
                <strong>Concept {i + 1}</strong>
                <Button type="button" disabled={saving} on:click={() => removeConcept(i)}>Remove</Button>
              </div>

              <div class="concept-grid">
                <div>
                  <Label forId={`concept_name_${i}`}>Name</Label>
                  <Input name={`concept_name_${i}`} bind:value={concept.name} />
                </div>

                <div>
                  <Label forId={`concept_type_${i}`}>Concept Type</Label>
                  <Select name={`concept_type_${i}`} bind:value={concept.type} options={conceptTypes} />
                </div>

                <div class="concept-full">
                  <Label forId={`concept_path_${i}`}>Path</Label>
                  <Input name={`concept_path_${i}`} bind:value={concept.path} />
                </div>

                <div>
                  <Label forId={`concept_prompt_source_${i}`}>Prompt Source</Label>
                  <Select
                    name={`concept_prompt_source_${i}`}
                    bind:value={concept.text.prompt_source}
                    options={promptSources}
                  />
                </div>

                <div>
                  <Label forId={`concept_prompt_path_${i}`}>Prompt Path</Label>
                  <Input name={`concept_prompt_path_${i}`} bind:value={concept.text.prompt_path} />
                </div>

                <div>
                  <Label forId={`concept_balancing_${i}`}>Balancing</Label>
                  <Input type="number" min={0} name={`concept_balancing_${i}`} bind:value={concept.balancing} />
                </div>

                <div>
                  <Label forId={`concept_balancing_strategy_${i}`}>Balancing Strategy</Label>
                  <Select
                    name={`concept_balancing_strategy_${i}`}
                    bind:value={concept.balancing_strategy}
                    options={balancingStrategies}
                  />
                </div>

                <div>
                  <Label forId={`concept_loss_weight_${i}`}>Loss Weight</Label>
                  <Input type="number" min={0} name={`concept_loss_weight_${i}`} bind:value={concept.loss_weight} />
                </div>

                <div>
                  <Label forId={`concept_image_variations_${i}`}>Image Variations</Label>
                  <Input
                    type="number"
                    min={1}
                    name={`concept_image_variations_${i}`}
                    bind:value={concept.image_variations}
                  />
                </div>

                <div>
                  <Label forId={`concept_text_variations_${i}`}>Text Variations</Label>
                  <Input
                    type="number"
                    min={1}
                    name={`concept_text_variations_${i}`}
                    bind:value={concept.text_variations}
                  />
                </div>

                <div class="switch-inline">
                  <Label forId={`concept_enabled_${i}`}>Enabled</Label>
                  <Switch name={`concept_enabled_${i}`} bind:checked={concept.enabled} />
                </div>

                <div class="switch-inline">
                  <Label forId={`concept_include_subdirectories_${i}`}>Include Subdirectories</Label>
                  <Switch
                    name={`concept_include_subdirectories_${i}`}
                    bind:checked={concept.include_subdirectories}
                  />
                </div>
              </div>
            </div>
          {/each}
        </div>

        <div class="action-row">
          <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save Concept Settings'}</Button>
          <Button type="button" disabled={saving} on:click={loadConceptsConfig}>Reload</Button>
        </div>
      </form>
    {/if}

    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
    {#if statusMessage}
      <p class="success">{statusMessage}</p>
    {/if}
  </Card>
</main>
