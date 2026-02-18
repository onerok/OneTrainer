/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BackupConfigResponse } from '../models/BackupConfigResponse';
import type { ConceptsConfigResponse } from '../models/ConceptsConfigResponse';
import type { DataConfigResponse } from '../models/DataConfigResponse';
import type { GeneralConfigResponse } from '../models/GeneralConfigResponse';
import type { LoraConfigResponse } from '../models/LoraConfigResponse';
import type { ModelConfigResponse } from '../models/ModelConfigResponse';
import type { SamplingConfigResponse } from '../models/SamplingConfigResponse';
import type { SaveBackupConfigRequest } from '../models/SaveBackupConfigRequest';
import type { SaveConceptsConfigRequest } from '../models/SaveConceptsConfigRequest';
import type { SaveDataConfigRequest } from '../models/SaveDataConfigRequest';
import type { SaveGeneralConfigRequest } from '../models/SaveGeneralConfigRequest';
import type { SaveLoraConfigRequest } from '../models/SaveLoraConfigRequest';
import type { SaveModelConfigRequest } from '../models/SaveModelConfigRequest';
import type { SaveSamplingConfigRequest } from '../models/SaveSamplingConfigRequest';
import type { SaveTrainingConfigRequest } from '../models/SaveTrainingConfigRequest';
import type { ToolsConfigResponse } from '../models/ToolsConfigResponse';
import type { TrainingConfigResponse } from '../models/TrainingConfigResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DefaultService {
    /**
     * Get General Config
     * @returns GeneralConfigResponse Successful Response
     * @throws ApiError
     */
    public static getGeneralConfigApiV1GeneralConfigGet(): CancelablePromise<GeneralConfigResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/general-config',
        });
    }
    /**
     * Save General Config
     * @returns GeneralConfigResponse Successful Response
     * @throws ApiError
     */
    public static saveGeneralConfigApiV1GeneralConfigPost({
        requestBody,
    }: {
        requestBody: SaveGeneralConfigRequest,
    }): CancelablePromise<GeneralConfigResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/general-config',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Health
     * @returns string Successful Response
     * @throws ApiError
     */
    public static healthApiV1HealthGet(): CancelablePromise<Record<string, string>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/health',
        });
    }
    /**
     * Get Model Config
     * @returns ModelConfigResponse Successful Response
     * @throws ApiError
     */
    public static getModelConfigApiV1ModelConfigGet(): CancelablePromise<ModelConfigResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/model-config',
        });
    }
    /**
     * Save Model Config
     * @returns ModelConfigResponse Successful Response
     * @throws ApiError
     */
    public static saveModelConfigApiV1ModelConfigPost({
        requestBody,
    }: {
        requestBody: SaveModelConfigRequest,
    }): CancelablePromise<ModelConfigResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/model-config',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Lora Config
     * @returns LoraConfigResponse Successful Response
     * @throws ApiError
     */
    public static getLoraConfigApiV1LoraConfigGet(): CancelablePromise<LoraConfigResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/lora-config',
        });
    }
    /**
     * Save Lora Config
     * @returns LoraConfigResponse Successful Response
     * @throws ApiError
     */
    public static saveLoraConfigApiV1LoraConfigPost({
        requestBody,
    }: {
        requestBody: SaveLoraConfigRequest,
    }): CancelablePromise<LoraConfigResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/lora-config',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Data Config
     * @returns DataConfigResponse Successful Response
     * @throws ApiError
     */
    public static getDataConfigApiV1DataConfigGet(): CancelablePromise<DataConfigResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/data-config',
        });
    }
    /**
     * Save Data Config
     * @returns DataConfigResponse Successful Response
     * @throws ApiError
     */
    public static saveDataConfigApiV1DataConfigPost({
        requestBody,
    }: {
        requestBody: SaveDataConfigRequest,
    }): CancelablePromise<DataConfigResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/data-config',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Backup Config
     * @returns BackupConfigResponse Successful Response
     * @throws ApiError
     */
    public static getBackupConfigApiV1BackupConfigGet(): CancelablePromise<BackupConfigResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/backup-config',
        });
    }
    /**
     * Save Backup Config
     * @returns BackupConfigResponse Successful Response
     * @throws ApiError
     */
    public static saveBackupConfigApiV1BackupConfigPost({
        requestBody,
    }: {
        requestBody: SaveBackupConfigRequest,
    }): CancelablePromise<BackupConfigResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/backup-config',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Sampling Config
     * @returns SamplingConfigResponse Successful Response
     * @throws ApiError
     */
    public static getSamplingConfigApiV1SamplingConfigGet(): CancelablePromise<SamplingConfigResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/sampling-config',
        });
    }
    /**
     * Save Sampling Config
     * @returns SamplingConfigResponse Successful Response
     * @throws ApiError
     */
    public static saveSamplingConfigApiV1SamplingConfigPost({
        requestBody,
    }: {
        requestBody: SaveSamplingConfigRequest,
    }): CancelablePromise<SamplingConfigResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/sampling-config',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Training Config
     * @returns TrainingConfigResponse Successful Response
     * @throws ApiError
     */
    public static getTrainingConfigApiV1TrainingConfigGet(): CancelablePromise<TrainingConfigResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/training-config',
        });
    }
    /**
     * Save Training Config
     * @returns TrainingConfigResponse Successful Response
     * @throws ApiError
     */
    public static saveTrainingConfigApiV1TrainingConfigPost({
        requestBody,
    }: {
        requestBody: SaveTrainingConfigRequest,
    }): CancelablePromise<TrainingConfigResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/training-config',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Concepts Config
     * @returns ConceptsConfigResponse Successful Response
     * @throws ApiError
     */
    public static getConceptsConfigApiV1ConceptsConfigGet(): CancelablePromise<ConceptsConfigResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/concepts-config',
        });
    }
    /**
     * Save Concepts Config
     * @returns ConceptsConfigResponse Successful Response
     * @throws ApiError
     */
    public static saveConceptsConfigApiV1ConceptsConfigPost({
        requestBody,
    }: {
        requestBody: SaveConceptsConfigRequest,
    }): CancelablePromise<ConceptsConfigResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/concepts-config',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Tools Config
     * @returns ToolsConfigResponse Successful Response
     * @throws ApiError
     */
    public static getToolsConfigApiV1ToolsConfigGet(): CancelablePromise<ToolsConfigResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tools-config',
        });
    }
}
