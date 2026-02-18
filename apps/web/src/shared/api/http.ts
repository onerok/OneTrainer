import { ApiError, OpenAPI } from '../../lib/api/generated';

export type ApiAction = 'load' | 'save';

export function configureApiBase(): void {
  OpenAPI.BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8011';
}

export async function withApiErrorHandling<T>(promise: Promise<T>, action: ApiAction): Promise<T> {
  try {
    return await promise;
  } catch (error) {
    if (error instanceof ApiError) {
      throw new Error(`Failed to ${action} config: ${error.status} ${error.statusText}`);
    }
    throw error instanceof Error ? error : new Error(`Failed to ${action} config`);
  }
}
