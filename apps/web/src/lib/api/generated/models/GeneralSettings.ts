/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GradientReducePrecisionValue } from './GradientReducePrecisionValue';
import type { TimeUnitValue } from './TimeUnitValue';
export type GeneralSettings = {
    workspace_dir: string;
    cache_dir: string;
    continue_last_backup: boolean;
    only_cache: boolean;
    debug_mode: boolean;
    debug_dir: string;
    tensorboard: boolean;
    tensorboard_always_on: boolean;
    tensorboard_expose: boolean;
    tensorboard_port: number;
    validation: boolean;
    validate_after: number;
    validate_after_unit: TimeUnitValue;
    dataloader_threads: number;
    train_device: string;
    multi_gpu: boolean;
    device_indexes: string;
    gradient_reduce_precision: GradientReducePrecisionValue;
    fused_gradient_reduce: boolean;
    async_gradient_reduce: boolean;
    async_gradient_reduce_buffer: number;
    temp_device: string;
};

