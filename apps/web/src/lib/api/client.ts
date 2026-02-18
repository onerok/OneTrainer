import { DefaultService } from './generated';
import { configureApiBase, withApiErrorHandling } from '../../shared/api/http';
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

configureApiBase();

export async function fetchGeneralConfig(): Promise<GeneralConfigResponse> {
  return withApiErrorHandling(DefaultService.getGeneralConfigApiV1GeneralConfigGet(), 'load');
}

export async function saveGeneralConfig(data: GeneralSettings): Promise<GeneralConfigResponse> {
  return withApiErrorHandling(
    DefaultService.saveGeneralConfigApiV1GeneralConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchModelConfig(): Promise<ModelConfigResponse> {
  return withApiErrorHandling(DefaultService.getModelConfigApiV1ModelConfigGet(), 'load');
}

export async function saveModelConfig(data: ModelSettings): Promise<ModelConfigResponse> {
  return withApiErrorHandling(
    DefaultService.saveModelConfigApiV1ModelConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchDataConfig(): Promise<DataConfigResponse> {
  return withApiErrorHandling(DefaultService.getDataConfigApiV1DataConfigGet(), 'load');
}

export async function saveDataConfig(data: DataSettings): Promise<DataConfigResponse> {
  return withApiErrorHandling(
    DefaultService.saveDataConfigApiV1DataConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchLoraConfig(): Promise<LoraConfigResponse> {
  return withApiErrorHandling(DefaultService.getLoraConfigApiV1LoraConfigGet(), 'load');
}

export async function saveLoraConfig(data: LoraSettings): Promise<LoraConfigResponse> {
  return withApiErrorHandling(
    DefaultService.saveLoraConfigApiV1LoraConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchBackupConfig(): Promise<BackupConfigResponse> {
  return withApiErrorHandling(DefaultService.getBackupConfigApiV1BackupConfigGet(), 'load');
}

export async function saveBackupConfig(data: BackupSettings): Promise<BackupConfigResponse> {
  return withApiErrorHandling(
    DefaultService.saveBackupConfigApiV1BackupConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchSamplingConfig(): Promise<SamplingConfigResponse> {
  return withApiErrorHandling(DefaultService.getSamplingConfigApiV1SamplingConfigGet(), 'load');
}

export async function saveSamplingConfig(data: SamplingSettings): Promise<SamplingConfigResponse> {
  return withApiErrorHandling(
    DefaultService.saveSamplingConfigApiV1SamplingConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchTrainingConfig(): Promise<TrainingConfigResponse> {
  return withApiErrorHandling(DefaultService.getTrainingConfigApiV1TrainingConfigGet(), 'load');
}

export async function saveTrainingConfig(data: TrainingSettings): Promise<TrainingConfigResponse> {
  return withApiErrorHandling(
    DefaultService.saveTrainingConfigApiV1TrainingConfigPost({ requestBody: { data } }),
    'save'
  );
}

export async function fetchToolsConfig(): Promise<ToolsConfigResponse> {
  return withApiErrorHandling(DefaultService.getToolsConfigApiV1ToolsConfigGet(), 'load');
}

export async function fetchConceptsConfig(): Promise<ConceptsConfigResponse> {
  return withApiErrorHandling(DefaultService.getConceptsConfigApiV1ConceptsConfigGet(), 'load');
}

export async function saveConceptsConfig(data: ConceptsSettings): Promise<ConceptsConfigResponse> {
  return withApiErrorHandling(
    DefaultService.saveConceptsConfigApiV1ConceptsConfigPost({ requestBody: { data } }),
    'save'
  );
}
