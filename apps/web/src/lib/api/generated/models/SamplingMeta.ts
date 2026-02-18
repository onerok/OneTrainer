/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AudioFormatValue } from './AudioFormatValue';
import type { ImageFormatValue } from './ImageFormatValue';
import type { NoiseSchedulerValue } from './NoiseSchedulerValue';
import type { TimeUnitValue } from './TimeUnitValue';
import type { VideoFormatValue } from './VideoFormatValue';
export type SamplingMeta = {
    sample_after_units: Array<TimeUnitValue>;
    sample_image_formats: Array<ImageFormatValue>;
    sample_video_formats: Array<VideoFormatValue>;
    sample_audio_formats: Array<AudioFormatValue>;
    noise_schedulers: Array<NoiseSchedulerValue>;
};

