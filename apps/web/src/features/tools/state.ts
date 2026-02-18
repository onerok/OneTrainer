import { fetchToolsConfig } from '../../lib/api/client';
import type { ToolInfo } from '../../lib/api/types';
import { loadConfigResource } from '../../app/configResource';
import { fromToolsResponse } from './adapter';

type LoadStateSetters = {
  setLoading: (value: boolean) => void;
  setErrorMessage: (value: string) => void;
  setStatusMessage: (value: string) => void;
};

type ToolsLoadArgs = {
  setToolsList: (value: ToolInfo[]) => void;
  markLoaded: () => void;
  stateSetters: LoadStateSetters;
};

export async function loadToolsState(args: ToolsLoadArgs): Promise<void> {
  const { setToolsList, markLoaded, stateSetters } = args;

  await loadConfigResource({
    request: fetchToolsConfig,
    onSuccess: (response) => {
      setToolsList(fromToolsResponse(response));
      markLoaded();
    },
    failureMessage: 'Failed to load Tools config',
    ...stateSetters
  });
}
