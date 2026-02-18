/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DataTypeValue } from './DataTypeValue';
import type { PeftTypeValue } from './PeftTypeValue';
export type LoraSettings = {
    peft_type: PeftTypeValue;
    lora_model_name: string;
    lora_rank: number;
    lora_alpha: number;
    lora_decompose: boolean;
    lora_decompose_norm_epsilon: boolean;
    lora_decompose_output_axis: boolean;
    lora_weight_dtype: DataTypeValue;
    bundle_additional_embeddings: boolean;
    dropout_probability: number;
    oft_block_size: number;
    oft_coft: boolean;
    coft_eps: number;
    oft_block_share: boolean;
};

