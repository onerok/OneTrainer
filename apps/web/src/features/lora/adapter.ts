import type { LoraConfigResponse, LoraSettings } from '../../lib/api/types';

export function fromLoraResponse(response: LoraConfigResponse): {
  form: LoraSettings;
  peftTypes: string[];
  loraWeightDtypes: string[];
} {
  return {
    form: response.data,
    peftTypes: response.meta.peft_types,
    loraWeightDtypes: response.meta.lora_weight_dtypes
  };
}

export function toLoraSavePayload(form: LoraSettings): LoraSettings {
  return {
    ...form,
    lora_rank: Number(form.lora_rank),
    lora_alpha: Number(form.lora_alpha),
    dropout_probability: Number(form.dropout_probability),
    oft_block_size: Number(form.oft_block_size),
    coft_eps: Number(form.coft_eps)
  };
}
