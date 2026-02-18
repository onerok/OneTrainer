/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AudioFormatValue } from './AudioFormatValue';
import type { ImageFormatValue } from './ImageFormatValue';
import type { SamplingSampleSettings } from './SamplingSampleSettings';
import type { TimeUnitValue } from './TimeUnitValue';
import type { VideoFormatValue } from './VideoFormatValue';
export type SamplingSettings_Output = {
    sample_definition_file_name: string;
    sample_after: number;
    sample_after_unit: TimeUnitValue;
    sample_skip_first: number;
    sample_image_format: ImageFormatValue;
    sample_video_format: VideoFormatValue;
    sample_audio_format: AudioFormatValue;
    samples_to_tensorboard: boolean;
    non_ema_sampling: boolean;
    samples: Array<SamplingSampleSettings>;
};

