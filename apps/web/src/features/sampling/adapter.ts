import type { SamplingConfigResponse, SamplingSettings } from '../../lib/api/types';

export function fromSamplingResponse(response: SamplingConfigResponse): {
  form: SamplingSettings;
  sampleAfterUnits: string[];
  sampleImageFormats: string[];
  sampleVideoFormats: string[];
  sampleAudioFormats: string[];
  noiseSchedulers: string[];
} {
  return {
    form: response.data,
    sampleAfterUnits: response.meta.sample_after_units,
    sampleImageFormats: response.meta.sample_image_formats,
    sampleVideoFormats: response.meta.sample_video_formats,
    sampleAudioFormats: response.meta.sample_audio_formats,
    noiseSchedulers: response.meta.noise_schedulers
  };
}

export function toSamplingSavePayload(form: SamplingSettings): SamplingSettings {
  return {
    ...form,
    sample_after: Number(form.sample_after),
    sample_skip_first: Number(form.sample_skip_first),
    samples: form.samples.map((sample) => ({
      ...sample,
      width: Number(sample.width),
      height: Number(sample.height),
      frames: Number(sample.frames),
      length: Number(sample.length),
      seed: Number(sample.seed),
      diffusion_steps: Number(sample.diffusion_steps),
      cfg_scale: Number(sample.cfg_scale),
      text_encoder_1_layer_skip: Number(sample.text_encoder_1_layer_skip),
      text_encoder_1_sequence_length:
        sample.text_encoder_1_sequence_length === null || sample.text_encoder_1_sequence_length === undefined
          ? null
          : Number(sample.text_encoder_1_sequence_length),
      text_encoder_2_layer_skip: Number(sample.text_encoder_2_layer_skip),
      text_encoder_2_sequence_length:
        sample.text_encoder_2_sequence_length === null || sample.text_encoder_2_sequence_length === undefined
          ? null
          : Number(sample.text_encoder_2_sequence_length),
      text_encoder_3_layer_skip: Number(sample.text_encoder_3_layer_skip),
      text_encoder_4_layer_skip: Number(sample.text_encoder_4_layer_skip)
    }))
  };
}
