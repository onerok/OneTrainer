import { ApiError, DefaultService, OpenAPI } from './generated';
import type {
  BackupConfigResponse,
  BackupSettings,
  ConceptsConfigResponse,
  ConceptsSettings,
  DataConfigResponse,
  DataSettings,
  GeneralConfigResponse,
  GeneralSettings,
  LoraConfigResponse,
  LoraSettings,
  ModelConfigResponse,
  ModelSettings,
  SamplingConfigResponse,
  SamplingSettings,
  ToolsConfigResponse,
  TrainingConfigResponse,
  TrainingSettings
} from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8011';
OpenAPI.BASE = API_BASE_URL;

async function wrapApiCall<T>(promise: Promise<T>, action: 'load' | 'save'): Promise<T> {
  try {
    return await promise;
  } catch (error) {
    if (error instanceof ApiError) {
      throw new Error(`Failed to ${action} config: ${error.status} ${error.statusText}`);
    }
    throw error instanceof Error ? error : new Error(`Failed to ${action} config`);
  }
}

export async function fetchGeneralConfig(): Promise<GeneralConfigResponse> {
  return wrapApiCall(DefaultService.getGeneralConfigApiV1GeneralConfigGet(), 'load');
}

export async function saveGeneralConfig(data: GeneralSettings): Promise<GeneralConfigResponse> {
  return wrapApiCall(
    DefaultService.saveGeneralConfigApiV1GeneralConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchModelConfig(): Promise<ModelConfigResponse> {
  return wrapApiCall(DefaultService.getModelConfigApiV1ModelConfigGet(), 'load');
}

export async function saveModelConfig(data: ModelSettings): Promise<ModelConfigResponse> {
  return wrapApiCall(
    DefaultService.saveModelConfigApiV1ModelConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchDataConfig(): Promise<DataConfigResponse> {
  return wrapApiCall(DefaultService.getDataConfigApiV1DataConfigGet(), 'load');
}

export async function saveDataConfig(data: DataSettings): Promise<DataConfigResponse> {
  return wrapApiCall(
    DefaultService.saveDataConfigApiV1DataConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchLoraConfig(): Promise<LoraConfigResponse> {
  return wrapApiCall(DefaultService.getLoraConfigApiV1LoraConfigGet(), 'load');
}

export async function saveLoraConfig(data: LoraSettings): Promise<LoraConfigResponse> {
  return wrapApiCall(
    DefaultService.saveLoraConfigApiV1LoraConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchBackupConfig(): Promise<BackupConfigResponse> {
  return wrapApiCall(DefaultService.getBackupConfigApiV1BackupConfigGet(), 'load');
}

export async function saveBackupConfig(data: BackupSettings): Promise<BackupConfigResponse> {
  return wrapApiCall(
    DefaultService.saveBackupConfigApiV1BackupConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchSamplingConfig(): Promise<SamplingConfigResponse> {
  return wrapApiCall(DefaultService.getSamplingConfigApiV1SamplingConfigGet(), 'load');
}

export async function saveSamplingConfig(data: SamplingSettings): Promise<SamplingConfigResponse> {
  return wrapApiCall(
    DefaultService.saveSamplingConfigApiV1SamplingConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchTrainingConfig(): Promise<TrainingConfigResponse> {
  return wrapApiCall(DefaultService.getTrainingConfigApiV1TrainingConfigGet(), 'load');
}

export async function saveTrainingConfig(data: TrainingSettings): Promise<TrainingConfigResponse> {
  return wrapApiCall(
    DefaultService.saveTrainingConfigApiV1TrainingConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchToolsConfig(): Promise<ToolsConfigResponse> {
  return wrapApiCall(DefaultService.getToolsConfigApiV1ToolsConfigGet(), 'load');
}

export async function fetchConceptsConfig(): Promise<ConceptsConfigResponse> {
  return wrapApiCall(DefaultService.getConceptsConfigApiV1ConceptsConfigGet(), 'load');
}

export async function saveConceptsConfig(data: ConceptsSettings): Promise<ConceptsConfigResponse> {
  return wrapApiCall(
    DefaultService.saveConceptsConfigApiV1ConceptsConfigPost({ requestBody: { data } }),
    'save'
  );
}
