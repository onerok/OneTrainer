/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TimeUnitValue } from './TimeUnitValue';
export type BackupSettings = {
    backup_after: number;
    backup_after_unit: TimeUnitValue;
    rolling_backup: boolean;
    rolling_backup_count: number;
    backup_before_save: boolean;
    save_every: number;
    save_every_unit: TimeUnitValue;
    save_skip_first: number;
    save_filename_prefix: string;
};

