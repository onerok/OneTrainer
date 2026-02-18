import type { DataConfigResponse, DataSettings } from '../../lib/api/types';

export function fromDataResponse(response: DataConfigResponse): DataSettings {
  return response.data;
}

export function toDataSavePayload(form: DataSettings): DataSettings {
  return form;
}
