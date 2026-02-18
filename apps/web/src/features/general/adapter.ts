import type { GeneralConfigResponse, GeneralSettings } from '../../lib/api/types';

export function fromGeneralResponse(response: GeneralConfigResponse): {
  form: GeneralSettings;
  validateAfterUnits: string[];
  gradientReducePrecisions: string[];
} {
  return {
    form: response.data,
    validateAfterUnits: response.meta.validate_after_units,
    gradientReducePrecisions: response.meta.gradient_reduce_precisions
  };
}

export function toGeneralSavePayload(form: GeneralSettings): GeneralSettings {
  return {
    ...form,
    tensorboard_port: Number(form.tensorboard_port),
    validate_after: Number(form.validate_after),
    dataloader_threads: Number(form.dataloader_threads),
    async_gradient_reduce_buffer: Number(form.async_gradient_reduce_buffer)
  };
}
