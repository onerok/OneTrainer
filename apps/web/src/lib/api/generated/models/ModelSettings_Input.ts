/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ConfigPartValue } from './ConfigPartValue';
import type { DataTypeValue } from './DataTypeValue';
import type { ModelFormatValue } from './ModelFormatValue';
import type { ModelPartSettings } from './ModelPartSettings';
import type { ModelTypeValue } from './ModelTypeValue';
import type { QuantizationSettings } from './QuantizationSettings';
import type { TrainingMethodValue } from './TrainingMethodValue';
export type ModelSettings_Input = {
    training_method: TrainingMethodValue;
    model_type: ModelTypeValue;
    huggingface_token: string;
    base_model_name: string;
    compile: boolean;
    unet: ModelPartSettings;
    prior: ModelPartSettings;
    transformer: ModelPartSettings;
    text_encoder: ModelPartSettings;
    text_encoder_2: ModelPartSettings;
    text_encoder_3: ModelPartSettings;
    text_encoder_4: ModelPartSettings;
    vae: ModelPartSettings;
    effnet_encoder: ModelPartSettings;
    decoder: ModelPartSettings;
    decoder_text_encoder: ModelPartSettings;
    decoder_vqgan: ModelPartSettings;
    quantization: QuantizationSettings;
    output_dtype: DataTypeValue;
    output_model_format: ModelFormatValue;
    output_model_destination: string;
    include_train_config: ConfigPartValue;
};

