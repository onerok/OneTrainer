import type { ModelConfigResponse, ModelSettings } from '../../lib/api/types';

export function fromModelResponse(response: ModelConfigResponse): {
  form: ModelSettings;
  trainingMethods: string[];
  modelTypes: string[];
  dataTypes: string[];
  outputDtypes: string[];
  modelFormats: string[];
  includeTrainConfigs: string[];
  quantizationPresets: string[];
} {
  return {
    form: response.data,
    trainingMethods: response.meta.training_methods,
    modelTypes: response.meta.model_types,
    dataTypes: response.meta.data_types,
    outputDtypes: response.meta.output_dtypes,
    modelFormats: response.meta.model_formats,
    includeTrainConfigs: response.meta.include_train_configs,
    quantizationPresets: response.meta.quantization_presets
  };
}

export function toModelSavePayload(form: ModelSettings): ModelSettings {
  return {
    ...form,
    quantization: {
      ...form.quantization,
      svd_rank: Number(form.quantization.svd_rank)
    }
  };
}
