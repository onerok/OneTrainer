type SetFlag = (value: boolean) => void;
type SetMessage = (value: string) => void;

type LoadConfigResourceArgs<TResponse> = {
  request: () => Promise<TResponse>;
  onSuccess: (response: TResponse) => void;
  failureMessage: string;
  setLoading: SetFlag;
  setErrorMessage: SetMessage;
  setStatusMessage: SetMessage;
};

type SaveConfigResourceArgs<TResponse> = {
  request: () => Promise<TResponse>;
  onSuccess: (response: TResponse) => void;
  successMessage: string;
  failureMessage: string;
  setSaving: SetFlag;
  setErrorMessage: SetMessage;
  setStatusMessage: SetMessage;
};

export async function loadConfigResource<TResponse>(args: LoadConfigResourceArgs<TResponse>): Promise<void> {
  const { request, onSuccess, failureMessage, setLoading, setErrorMessage, setStatusMessage } = args;

  setLoading(true);
  setErrorMessage('');
  setStatusMessage('');

  try {
    const response = await request();
    onSuccess(response);
  } catch (error) {
    setErrorMessage(error instanceof Error ? error.message : failureMessage);
  } finally {
    setLoading(false);
  }
}

export async function saveConfigResource<TResponse>(args: SaveConfigResourceArgs<TResponse>): Promise<void> {
  const { request, onSuccess, successMessage, failureMessage, setSaving, setErrorMessage, setStatusMessage } = args;

  setSaving(true);
  setErrorMessage('');
  setStatusMessage('');

  try {
    const response = await request();
    onSuccess(response);
    setStatusMessage(successMessage);
  } catch (error) {
    setErrorMessage(error instanceof Error ? error.message : failureMessage);
  } finally {
    setSaving(false);
  }
}
