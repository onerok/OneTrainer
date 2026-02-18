<script lang="ts">
  import { onMount } from 'svelte';
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
  import Card from '../lib/components/ui/Card.svelte';
  import Tabs from '../lib/components/ui/Tabs.svelte';
  import BackupTab from '../features/backup/BackupTab.svelte';
  import { loadBackupState, saveBackupState } from '../features/backup/state';
  import ConceptsTab from '../features/concepts/ConceptsTab.svelte';
  import { loadConceptsState, saveConceptsState } from '../features/concepts/state';
  import DataTab from '../features/data/DataTab.svelte';
  import { loadDataState, saveDataState } from '../features/data/state';
  import GeneralTab from '../features/general/GeneralTab.svelte';
  import { loadGeneralState, saveGeneralState } from '../features/general/state';
  import LoraTab from '../features/lora/LoraTab.svelte';
  import { loadLoraState, saveLoraState } from '../features/lora/state';
  import ModelTab from '../features/model/ModelTab.svelte';
  import { loadModelState, saveModelState } from '../features/model/state';
  import SamplingTab from '../features/sampling/SamplingTab.svelte';
  import { loadSamplingState, saveSamplingState } from '../features/sampling/state';
  import TrainingTab from '../features/training/TrainingTab.svelte';
  import { loadTrainingState, saveTrainingState } from '../features/training/state';
  import ToolsTab from '../features/tools/ToolsTab.svelte';
  import { loadToolsState } from '../features/tools/state';
  import { createTabBooleanState, createTabStringState } from '../shared/state/ui';
  import type { TabId } from './routes';

  let activeTab: TabId = 'general';

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

  let loadedByTab = createTabBooleanState(false);
  let loadingByTab = createTabBooleanState(false);
  let savingByTab = createTabBooleanState(false);
  let statusByTab = createTabStringState('');
  let errorByTab = createTabStringState('');
  let loading = true;
  let saving = false;
  let statusMessage = '';
  let errorMessage = '';

  loadingByTab = { ...loadingByTab, [activeTab]: true };

  $: loading = loadingByTab[activeTab];
  $: saving = savingByTab[activeTab];
  $: statusMessage = statusByTab[activeTab];
  $: errorMessage = errorByTab[activeTab];

  function setTabLoading(tabId: TabId, value: boolean) {
    loadingByTab = { ...loadingByTab, [tabId]: value };
  }

  function setTabSaving(tabId: TabId, value: boolean) {
    savingByTab = { ...savingByTab, [tabId]: value };
  }

  function setTabStatusMessage(tabId: TabId, value: string) {
    statusByTab = { ...statusByTab, [tabId]: value };
  }

  function setTabErrorMessage(tabId: TabId, value: string) {
    errorByTab = { ...errorByTab, [tabId]: value };
  }

  function markTabLoaded(tabId: TabId) {
    loadedByTab = { ...loadedByTab, [tabId]: true };
  }

  function loadStateSetters(tabId: TabId) {
    return {
      setLoading: (value: boolean) => setTabLoading(tabId, value),
      setErrorMessage: (value: string) => setTabErrorMessage(tabId, value),
      setStatusMessage: (value: string) => setTabStatusMessage(tabId, value)
    };
  }

  function saveStateSetters(tabId: TabId) {
    return {
      setSaving: (value: boolean) => setTabSaving(tabId, value),
      setErrorMessage: (value: string) => setTabErrorMessage(tabId, value),
      setStatusMessage: (value: string) => setTabStatusMessage(tabId, value)
    };
  }

  onMount(async () => {
    await ensureTabLoaded(activeTab);
  });

  async function ensureTabLoaded(tabId: TabId) {
    if (loadedByTab[tabId]) {
      return;
    }

    if (tabId === 'general') {
      await loadGeneralConfig();
      return;
    }
    if (tabId === 'model') {
      await loadModelConfig();
      return;
    }
    if (tabId === 'lora') {
      await loadLoraConfig();
      return;
    }
    if (tabId === 'data') {
      await loadDataConfig();
      return;
    }
    if (tabId === 'backup') {
      await loadBackupConfig();
      return;
    }
    if (tabId === 'sampling') {
      await loadSamplingConfig();
      return;
    }
    if (tabId === 'training') {
      await loadTrainingConfig();
      return;
    }
    if (tabId === 'tools') {
      await loadToolsConfig();
      return;
    }
    if (tabId === 'concepts') {
      await loadConceptsConfig();
    }
  }

  async function loadGeneralConfig() {
    const tabId: TabId = 'general';
    await loadGeneralState({
      setGeneralForm: (value) => {
        generalForm = value;
      },
      setValidateAfterUnits: (value) => {
        validateAfterUnits = value;
      },
      setGradientReducePrecisions: (value) => {
        gradientReducePrecisions = value;
      },
      markLoaded: () => markTabLoaded(tabId),
      stateSetters: loadStateSetters(tabId)
    });
  }

  async function loadModelConfig() {
    const tabId: TabId = 'model';
    await loadModelState({
      setModelForm: (value) => {
        modelForm = value;
      },
      setTrainingMethods: (value) => {
        trainingMethods = value;
      },
      setModelTypes: (value) => {
        modelTypes = value;
      },
      setDataTypes: (value) => {
        dataTypes = value;
      },
      setOutputDtypes: (value) => {
        outputDtypes = value;
      },
      setModelFormats: (value) => {
        modelFormats = value;
      },
      setIncludeTrainConfigs: (value) => {
        includeTrainConfigs = value;
      },
      setQuantizationPresets: (value) => {
        quantizationPresets = value;
      },
      markLoaded: () => markTabLoaded(tabId),
      stateSetters: loadStateSetters(tabId)
    });
  }

  async function loadDataConfig() {
    const tabId: TabId = 'data';
    await loadDataState({
      setDataForm: (value) => {
        dataForm = value;
      },
      markLoaded: () => markTabLoaded(tabId),
      stateSetters: loadStateSetters(tabId)
    });
  }

  async function loadLoraConfig() {
    const tabId: TabId = 'lora';
    await loadLoraState({
      setLoraForm: (value) => {
        loraForm = value;
      },
      setPeftTypes: (value) => {
        peftTypes = value;
      },
      setLoraWeightDtypes: (value) => {
        loraWeightDtypes = value;
      },
      markLoaded: () => markTabLoaded(tabId),
      stateSetters: loadStateSetters(tabId)
    });
  }

  async function loadConceptsConfig() {
    const tabId: TabId = 'concepts';
    await loadConceptsState({
      setConceptsForm: (value) => {
        conceptsForm = value;
      },
      setConceptTypes: (value) => {
        conceptTypes = value;
      },
      setBalancingStrategies: (value) => {
        balancingStrategies = value;
      },
      setPromptSources: (value) => {
        promptSources = value;
      },
      markLoaded: () => markTabLoaded(tabId),
      stateSetters: loadStateSetters(tabId)
    });
  }

  async function loadBackupConfig() {
    const tabId: TabId = 'backup';
    await loadBackupState({
      setBackupForm: (value) => {
        backupForm = value;
      },
      setBackupAfterUnits: (value) => {
        backupAfterUnits = value;
      },
      setSaveEveryUnits: (value) => {
        saveEveryUnits = value;
      },
      markLoaded: () => markTabLoaded(tabId),
      stateSetters: loadStateSetters(tabId)
    });
  }

  async function loadSamplingConfig() {
    const tabId: TabId = 'sampling';
    await loadSamplingState({
      setSamplingForm: (value) => {
        samplingForm = value;
      },
      setSampleAfterUnits: (value) => {
        sampleAfterUnits = value;
      },
      setSampleImageFormats: (value) => {
        sampleImageFormats = value;
      },
      setSampleVideoFormats: (value) => {
        sampleVideoFormats = value;
      },
      setSampleAudioFormats: (value) => {
        sampleAudioFormats = value;
      },
      setNoiseSchedulers: (value) => {
        noiseSchedulers = value;
      },
      markLoaded: () => markTabLoaded(tabId),
      stateSetters: loadStateSetters(tabId)
    });
  }

  async function loadTrainingConfig() {
    const tabId: TabId = 'training';
    await loadTrainingState({
      setTrainingForm: (value) => {
        trainingForm = value;
      },
      setTrainingClipGradNorm: (value) => {
        trainingClipGradNorm = value;
      },
      setOptimizers: (value) => {
        optimizers = value;
      },
      setLearningRateSchedulers: (value) => {
        learningRateSchedulers = value;
      },
      setLearningRateScalers: (value) => {
        learningRateScalers = value;
      },
      setEmaModes: (value) => {
        emaModes = value;
      },
      setGradientCheckpointingMethods: (value) => {
        gradientCheckpointingMethods = value;
      },
      setTrainDtypes: (value) => {
        trainDtypes = value;
      },
      setFallbackTrainDtypes: (value) => {
        fallbackTrainDtypes = value;
      },
      markLoaded: () => markTabLoaded(tabId),
      stateSetters: loadStateSetters(tabId)
    });
  }

  async function loadToolsConfig() {
    const tabId: TabId = 'tools';
    await loadToolsState({
      setToolsList: (value) => {
        toolsList = value;
      },
      markLoaded: () => markTabLoaded(tabId),
      stateSetters: loadStateSetters(tabId)
    });
  }

  async function onSubmitGeneral(event: SubmitEvent) {
    event.preventDefault();
    if (!generalForm) {
      return;
    }
    const tabId: TabId = 'general';
    await saveGeneralState({
      generalForm,
      setGeneralForm: (value) => {
        generalForm = value;
      },
      stateSetters: saveStateSetters(tabId)
    });
  }

  async function onSubmitModel(event: SubmitEvent) {
    event.preventDefault();
    if (!modelForm) {
      return;
    }
    const tabId: TabId = 'model';
    await saveModelState({
      modelForm,
      setModelForm: (value) => {
        modelForm = value;
      },
      stateSetters: saveStateSetters(tabId)
    });
  }

  async function onSubmitData(event: SubmitEvent) {
    event.preventDefault();
    if (!dataForm) {
      return;
    }
    const tabId: TabId = 'data';
    await saveDataState({
      dataForm,
      setDataForm: (value) => {
        dataForm = value;
      },
      stateSetters: saveStateSetters(tabId)
    });
  }

  async function onSubmitLora(event: SubmitEvent) {
    event.preventDefault();
    if (!loraForm) {
      return;
    }
    const tabId: TabId = 'lora';
    await saveLoraState({
      loraForm,
      setLoraForm: (value) => {
        loraForm = value;
      },
      stateSetters: saveStateSetters(tabId)
    });
  }

  async function onSubmitConcepts(event: SubmitEvent) {
    event.preventDefault();
    if (!conceptsForm) {
      return;
    }
    const tabId: TabId = 'concepts';
    await saveConceptsState({
      conceptsForm,
      setConceptsForm: (value) => {
        conceptsForm = value;
      },
      stateSetters: saveStateSetters(tabId)
    });
  }

  async function onSubmitBackup(event: SubmitEvent) {
    event.preventDefault();
    if (!backupForm) {
      return;
    }
    const tabId: TabId = 'backup';
    await saveBackupState({
      backupForm,
      setBackupForm: (value) => {
        backupForm = value;
      },
      stateSetters: saveStateSetters(tabId)
    });
  }

  async function onSubmitSampling(event: SubmitEvent) {
    event.preventDefault();
    if (!samplingForm) {
      return;
    }
    const tabId: TabId = 'sampling';
    await saveSamplingState({
      samplingForm,
      setSamplingForm: (value) => {
        samplingForm = value;
      },
      stateSetters: saveStateSetters(tabId)
    });
  }

  async function onSubmitTraining(event: SubmitEvent) {
    event.preventDefault();
    if (!trainingForm) {
      return;
    }
    const tabId: TabId = 'training';
    await saveTrainingState({
      trainingForm,
      trainingClipGradNorm,
      setTrainingForm: (value) => {
        trainingForm = value;
      },
      setTrainingClipGradNorm: (value) => {
        trainingClipGradNorm = value;
      },
      stateSetters: saveStateSetters(tabId)
    });
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

  async function onTabChange(event: CustomEvent<{ tabId: TabId }>) {
    activeTab = event.detail.tabId;
    if (!loadedByTab[activeTab]) {
      setTabLoading(activeTab, true);
    }
    await ensureTabLoaded(activeTab);
  }

  async function onToolAction(tool: ToolInfo) {
    const tabId: TabId = 'tools';
    if (tool.action_type === 'WEB_LINK') {
      window.open(tool.action_value, '_blank', 'noopener,noreferrer');
      setTabStatusMessage(tabId, `${tool.name} opened.`);
      return;
    }

    if (tool.action_type === 'CLI_COMMAND') {
      try {
        await navigator.clipboard.writeText(tool.action_value);
        setTabStatusMessage(tabId, `${tool.name} command copied: ${tool.action_value}`);
      } catch {
        setTabStatusMessage(tabId, `${tool.name} command: ${tool.action_value}`);
      }
      return;
    }

    setTabStatusMessage(tabId, tool.action_value);
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
    {:else if activeTab === 'tools' && !loadedByTab.tools}
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
