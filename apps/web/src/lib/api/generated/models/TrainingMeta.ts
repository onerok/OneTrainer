/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DataTypeValue } from './DataTypeValue';
import type { EMAModeValue } from './EMAModeValue';
import type { GradientCheckpointingMethodValue } from './GradientCheckpointingMethodValue';
import type { LearningRateScalerValue } from './LearningRateScalerValue';
import type { LearningRateSchedulerValue } from './LearningRateSchedulerValue';
export type TrainingMeta = {
    optimizers: Array<string>;
    learning_rate_schedulers: Array<LearningRateSchedulerValue>;
    learning_rate_scalers: Array<LearningRateScalerValue>;
    ema_modes: Array<EMAModeValue>;
    gradient_checkpointing_methods: Array<GradientCheckpointingMethodValue>;
    train_dtypes: Array<DataTypeValue>;
    fallback_train_dtypes: Array<DataTypeValue>;
};

