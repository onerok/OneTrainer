import type { TrainingConfigResponse, TrainingSettings } from '../../lib/api/types';

export function fromTrainingResponse(response: TrainingConfigResponse): {
  form: TrainingSettings;
  trainingClipGradNorm: number | '';
  optimizers: string[];
  learningRateSchedulers: string[];
  learningRateScalers: string[];
  emaModes: string[];
  gradientCheckpointingMethods: string[];
  trainDtypes: string[];
  fallbackTrainDtypes: string[];
} {
  return {
    form: response.data,
    trainingClipGradNorm: response.data.clip_grad_norm ?? '',
    optimizers: response.meta.optimizers,
    learningRateSchedulers: response.meta.learning_rate_schedulers,
    learningRateScalers: response.meta.learning_rate_scalers,
    emaModes: response.meta.ema_modes,
    gradientCheckpointingMethods: response.meta.gradient_checkpointing_methods,
    trainDtypes: response.meta.train_dtypes,
    fallbackTrainDtypes: response.meta.fallback_train_dtypes
  };
}

export function toTrainingSavePayload(form: TrainingSettings, trainingClipGradNorm: number | ''): TrainingSettings {
  return {
    ...form,
    learning_rate: Number(form.learning_rate),
    learning_rate_warmup_steps: Number(form.learning_rate_warmup_steps),
    learning_rate_min_factor: Number(form.learning_rate_min_factor),
    learning_rate_cycles: Number(form.learning_rate_cycles),
    epochs: Number(form.epochs),
    batch_size: Number(form.batch_size),
    gradient_accumulation_steps: Number(form.gradient_accumulation_steps),
    clip_grad_norm: trainingClipGradNorm === '' ? null : Number(trainingClipGradNorm),
    ema_decay: Number(form.ema_decay),
    ema_update_step_interval: Number(form.ema_update_step_interval),
    layer_offload_fraction: Number(form.layer_offload_fraction)
  };
}
