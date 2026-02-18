/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DataTypeValue } from './DataTypeValue';
import type { EMAModeValue } from './EMAModeValue';
import type { GradientCheckpointingMethodValue } from './GradientCheckpointingMethodValue';
import type { LearningRateScalerValue } from './LearningRateScalerValue';
import type { LearningRateSchedulerValue } from './LearningRateSchedulerValue';
export type TrainingSettings = {
    optimizer: string;
    learning_rate_scheduler: LearningRateSchedulerValue;
    learning_rate: number;
    learning_rate_warmup_steps: number;
    learning_rate_min_factor: number;
    learning_rate_cycles: number;
    epochs: number;
    batch_size: number;
    gradient_accumulation_steps: number;
    learning_rate_scaler: LearningRateScalerValue;
    clip_grad_norm?: (number | null);
    ema: EMAModeValue;
    ema_decay: number;
    ema_update_step_interval: number;
    gradient_checkpointing: GradientCheckpointingMethodValue;
    layer_offload_fraction: number;
    train_dtype: DataTypeValue;
    fallback_train_dtype: DataTypeValue;
    enable_autocast_cache: boolean;
    resolution: string;
    force_circular_padding: boolean;
};

