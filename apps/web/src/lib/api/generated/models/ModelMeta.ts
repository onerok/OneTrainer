/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ConfigPartValue } from './ConfigPartValue';
import type { DataTypeValue } from './DataTypeValue';
import type { ModelFormatValue } from './ModelFormatValue';
import type { ModelTypeValue } from './ModelTypeValue';
import type { TrainingMethodValue } from './TrainingMethodValue';
export type ModelMeta = {
    training_methods: Array<TrainingMethodValue>;
    model_types: Array<ModelTypeValue>;
    data_types: Array<DataTypeValue>;
    output_dtypes: Array<DataTypeValue>;
    model_formats: Array<ModelFormatValue>;
    include_train_configs: Array<ConfigPartValue>;
    quantization_presets: Array<string>;
};

