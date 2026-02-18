import type { ToolInfo, ToolsConfigResponse } from '../../lib/api/types';

export function fromToolsResponse(response: ToolsConfigResponse): ToolInfo[] {
  return response.data.tools;
}
