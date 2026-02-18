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
  import ConceptsTab from '../features/concepts/ConceptsTab.svelte';
  import DataTab from '../features/data/DataTab.svelte';
  import GeneralTab from '../features/general/GeneralTab.svelte';
  import LoraTab from '../features/lora/LoraTab.svelte';
  import ModelTab from '../features/model/ModelTab.svelte';
  import SamplingTab from '../features/sampling/SamplingTab.svelte';
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
      <GeneralTab
        {generalForm}
        {validateAfterUnits}
        {gradientReducePrecisions}
        {saving}
        onSubmit={onSubmitGeneral}
        onReload={loadGeneralConfig}
      />
    {:else if activeTab === 'model' && modelForm}
      <ModelTab
        {modelForm}
        {trainingMethods}
        {modelTypes}
        {dataTypes}
        {outputDtypes}
        {modelFormats}
        {includeTrainConfigs}
        {quantizationPresets}
        {saving}
        onSubmit={onSubmitModel}
        onReload={loadModelConfig}
      />
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
      <SamplingTab
        {samplingForm}
        {sampleAfterUnits}
        {sampleImageFormats}
        {sampleVideoFormats}
        {sampleAudioFormats}
        {noiseSchedulers}
        {saving}
        onSubmit={onSubmitSampling}
        onReload={loadSamplingConfig}
        {addSample}
        {removeSample}
      />
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
      <ConceptsTab
        {conceptsForm}
        {conceptTypes}
        {balancingStrategies}
        {promptSources}
        {saving}
        onSubmit={onSubmitConcepts}
        onReload={loadConceptsConfig}
        {addConcept}
        {removeConcept}
      />
    {/if}

    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
    {#if statusMessage}
      <p class="success">{statusMessage}</p>
    {/if}
  </Card>
</main>
