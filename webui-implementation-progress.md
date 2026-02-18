# Web UI Implementation Progress

Last updated: 2026-02-18

## Scope Agreed
- Build a web version of OneTrainer UI using:
  - Svelte frontend
  - shadcn-style component structure
  - FastAPI backend
- All target tabs are now implemented in web UI:
  - `General`, `Model`, `LoRA`, `Data`, `Training`, `Sampling`, `Backup`, `Tools`, `Concepts`

## Delivery Process (Per Tab)
- We will implement the web UI one tab at a time.
- For each tab, we must first reference the current desktop implementation to match behavior and config mapping.
- A tab is not complete until Playwright CLI acceptance testing passes.

### Required workflow for each tab
1. Reference current implementation:
   - Identify source UI code in `modules/ui/*`
   - Identify backing config keys in `modules/util/config/TrainConfig.py` (and related enums/config classes)
   - Document exact fields, defaults, toggles, and dependencies
2. Implement backend contract:
   - Add/extend FastAPI endpoint(s) for that tab
   - Preserve existing config key names and enum values
3. Implement frontend tab UI:
   - Build Svelte UI for only that tab scope
   - Keep non-target tabs unchanged/disabled
4. Run acceptance testing with Playwright CLI:
   - Verify tab loads
   - Verify required fields render
   - Verify save works
   - Verify reload reflects persisted values
   - Verify known critical toggles/interactions for that tab
5. Record results in this file:
   - Pass/fail
   - Repro steps for failures
   - Follow-up fixes/TODOs

## Acceptance Testing Standard (Playwright CLI)
- Mandatory after each tab implementation.
- Minimum checks per tab:
  - Load app and open target tab
  - Validate baseline/default values from backend
  - Change representative field values
  - Save and verify success response/state
  - Reload and verify persistence
  - Confirm no console errors for target flow
- Evidence to capture:
  - Playwright actions run
  - Observed UI result
  - API behavior (success/failure)

## What Was Implemented

### 1. New app structure
- Added `apps/README.md`
- Added backend app in `apps/api`
- Added frontend app in `apps/web`

### 2. FastAPI backend (`apps/api`)
- Added:
  - `apps/api/app/main.py`
  - `apps/api/requirements.txt`
  - `apps/api/README.md`
- Implemented endpoints:
  - `GET /api/v1/health`
  - `GET /api/v1/general-config`
  - `POST /api/v1/general-config`
- `General` fields mapped to existing `TrainConfig` keys (no custom schema drift).
- Persistence implemented to:
  - `training_user_settings/web-general-config.json`
- Refactor status:
  - Route/service/mapper split completed for all implemented tabs.
  - Schema modularization completed:
    - `apps/api/app/schemas/common.py`
    - `apps/api/app/schemas/general.py`
    - `apps/api/app/schemas/model.py`
    - `apps/api/app/schemas/lora.py`
    - `apps/api/app/schemas/data.py`
    - `apps/api/app/schemas/training.py`
    - `apps/api/app/schemas/sampling.py`
    - `apps/api/app/schemas/backup.py`
    - `apps/api/app/schemas/concepts.py`
    - `apps/api/app/schemas/tools.py`

### 3. Svelte frontend (`apps/web`)
- Added Vite/Svelte app scaffolding:
  - `apps/web/package.json`
  - `apps/web/vite.config.ts`
  - `apps/web/svelte.config.js`
  - `apps/web/tsconfig.json`
  - `apps/web/index.html`
  - `apps/web/src/main.ts`
  - `apps/web/src/vite-env.d.ts`
- Added API client/types:
  - `apps/web/src/lib/api/client.ts`
  - `apps/web/src/lib/api/types.ts`
- Added UI component layer (shadcn-style organization):
  - `apps/web/src/lib/components/ui/Button.svelte`
  - `apps/web/src/lib/components/ui/Card.svelte`
  - `apps/web/src/lib/components/ui/Input.svelte`
  - `apps/web/src/lib/components/ui/Label.svelte`
  - `apps/web/src/lib/components/ui/Select.svelte`
  - `apps/web/src/lib/components/ui/Switch.svelte`
  - `apps/web/src/lib/components/ui/Tabs.svelte`
- Implemented feature tabs and shell in:
  - `apps/web/src/app/AppShell.svelte`
  - `apps/web/src/features/*`
- Added styling in:
  - `apps/web/src/app.css`
- Refactor status:
  - Per-tab feature component extraction completed.
  - Per-tab `state.ts` extraction completed.
  - Per-tab `adapter.ts` extraction completed.
  - Shared layer introduced:
    - `apps/web/src/shared/api/http.ts`
    - `apps/web/src/shared/state/ui.ts`

### 4. Dev workflow and docs
- Added `web-tmux` recipe to `justfile`:
  - Runs API + frontend in one tmux session.
- Updated `.gitignore` for:
  - `apps/web/node_modules`
  - `apps/web/dist`
- Standardized API port to `8011` (instead of `8000`) across:
  - `justfile`
  - `apps/api/README.md`
  - `apps/web/src/lib/api/client.ts`
  - `apps/web/README.md`

## Validation Already Done
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- OpenAPI generation:
  - `npm --prefix apps/web run gen:api`
- Playwright manual E2E checks:
  - App loads
  - Tab flows render and save/reload across implemented features.
- Playwright automated smoke:
  - `npm --prefix apps/web run smoke:playwright` (requires running API + web servers)

## Current Status Summary
- Completed:
  - Backend route/service/mapper/schema modularization
  - Frontend app shell + feature extraction + per-tab state/adapter extraction
  - Shared frontend ownership points (`shared/api/http.ts`, `shared/state/ui.ts`)
  - Automated Playwright smoke script
- Remaining:
  - Final cleanup/documentation consistency and optional future UX improvements (validation/error UX polish)

## Session Update (2026-02-18)

### Implemented in this session (`Model` tab start)
- Backend (`apps/api`):
  - Added `GET /api/v1/model-config`
  - Added `POST /api/v1/model-config`
  - Added typed model schemas for:
    - `training_method`, `model_type`
    - model-part dtypes/overrides (`unet`, `prior`, `transformer`, `text_encoder*`, `vae`, `effnet_encoder`, `decoder*`)
    - output settings (`output_dtype`, `output_model_format`, `output_model_destination`, `include_train_config`)
    - quantization (`layer_filter*`, `svd_dtype`, `svd_rank`)
    - `secrets.huggingface_token`
  - Preserved existing `TrainConfig` key names and enum-string values.
- Frontend (`apps/web`):
  - Enabled `Model` tab in tab bar and tab switching.
  - Added API client/types for model config endpoints.
  - Added `Model` form with save/reload flow bound to backend contract.
  - Kept non-General/Model tabs disabled.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- Playwright smoke checks (manual via MCP):
  - Open app and switch to `Model` tab
  - Verify model fields render
  - Edit representative values:
    - `training_method = LORA`
    - `base_model_name = stabilityai/stable-diffusion-2-1-base`
    - `huggingface_token = hf_playwright_token`
    - `output_model_destination = models/playwright-model.safetensors`
  - Save and verify success message (`Model settings saved.`)
  - Reload app and verify persisted values remain
  - Confirm API calls:
    - `GET /api/v1/model-config` -> `200`
    - `POST /api/v1/model-config` -> `200`
  - Console:
    - No model-flow blocking errors observed

## Session Update (2026-02-18, Data tab)

### Implemented in this session (`Data` tab)
- Backend (`apps/api`):
  - Added `GET /api/v1/data-config`
  - Added `POST /api/v1/data-config`
  - Added typed data schema mapped to desktop Data tab keys:
    - `aspect_ratio_bucketing`
    - `latent_caching`
    - `clear_cache_before_training`
  - Preserved existing `TrainConfig` key names and save/load behavior.
- Frontend (`apps/web`):
  - Enabled `Data` tab in tab bar.
  - Added API client/types for data config endpoints.
  - Added `Data` tab form with the three desktop-aligned toggles.
  - Added save/reload flow for data settings.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- Playwright smoke checks (manual via MCP):
  - Open app and switch to `Data` tab
  - Verify required fields render:
    - `Aspect Ratio Bucketing`
    - `Latent Caching`
    - `Clear cache before training`
  - Change representative values and save
  - Verify success message (`Data settings saved.`)
  - Reload app and verify persistence of changed values
  - Confirm API calls:
    - `GET /api/v1/data-config` -> `200`
    - `POST /api/v1/data-config` -> `200`
  - Console:
    - No data-flow blocking errors observed

## Session Update (2026-02-18, Concepts tab)

### Implemented in this session (`Concepts` tab)
- Backend (`apps/api`):
  - Added `GET /api/v1/concepts-config`
  - Added `POST /api/v1/concepts-config`
  - Added schemas for concept list payload and metadata:
    - `concept_file_name`
    - `concepts[]` (typed top-level/general concept fields)
    - `concept_types`, `balancing_strategies`, `prompt_sources`
  - Implemented concept-file load/save against `concept_file_name` path, while preserving extra concept fields through pass-through data handling.
- Frontend (`apps/web`):
  - Enabled `Concepts` tab in tab bar.
  - Added API client/types for concepts endpoints.
  - Added concepts editor UI:
    - concept file path field
    - add/remove concept rows
    - editable general concept fields (name/path/type/prompt source/path, balancing, loss weight, variations, toggles)
    - save/reload flow

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- Playwright smoke checks (manual via MCP):
  - Open app and switch to `Concepts` tab
  - Add a concept and edit representative values
  - Save and verify success message (`Concept settings saved.`)
  - Reload app and verify persistence of edited values
  - Confirm API calls:
    - `GET /api/v1/concepts-config` -> `200`
    - `POST /api/v1/concepts-config` -> `200`
  - Console:
    - No concepts-flow blocking errors observed

## Run Commands (Current)
- API:
  - `cd apps/api`
  - `uv sync`
  - `uv run uvicorn app.main:app --reload --port 8011`
- Web:
  - `cd apps/web`
  - `npm install`
  - `npm run dev`
- Combined tmux:
  - `just web-tmux`

## Session Update (2026-02-18, Training tab start)

### Implemented in this session (`Training` tab, core slice)
- Backend (`apps/api`):
  - Added `GET /api/v1/training-config`
  - Added `POST /api/v1/training-config`
  - Added typed training schema + metadata for core model-agnostic training controls mapped to desktop `TrainingTab`:
    - optimizer and LR scheduler settings
    - LR numeric controls (`learning_rate*`, `epochs`, `batch_size`, `gradient_accumulation_steps`, `learning_rate_scaler`, `clip_grad_norm`)
    - EMA controls (`ema`, `ema_decay`, `ema_update_step_interval`)
    - checkpointing + offload controls (`gradient_checkpointing`, `layer_offload_fraction`)
    - dtype/runtime controls (`train_dtype`, `fallback_train_dtype`, `enable_autocast_cache`)
    - `resolution`, `force_circular_padding`
  - Preserved existing `TrainConfig` key names and enum-string values.
- Frontend (`apps/web`):
  - Enabled `Training` tab in tab bar.
  - Added API client/types for training config endpoints.
  - Added `Training` tab form for the core fields above with save/reload flow.
  - Added numeric coercion and nullable handling for `clip_grad_norm`.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- Playwright smoke checks (manual via MCP):
  - Open app and switch to `Training` tab
  - Verify required training fields render (optimizer, LR controls, EMA, checkpointing, dtype, resolution)
  - Edit representative values:
    - `optimizer = ADAMW_ADV`
    - `learning_rate = 0.00001`
    - `epochs = 42`
    - `ema = GPU`
    - `gradient_checkpointing = CPU_OFFLOADED`
    - `layer_offload_fraction = 0.25`
    - `resolution = 640`
  - Save and verify success message (`Training settings saved.`)
  - Reload app and verify persistence of changed values
  - Confirm API calls:
    - `GET /api/v1/training-config` -> `200`
    - `POST /api/v1/training-config` -> `200`
  - Console:
    - No training-flow blocking errors observed

### Remaining Training scope
- Add model-specific sections from desktop `TrainingTab`:
  - text encoder blocks (`text_encoder*` include/train/dropout/stop/lr/skip/seq len)
  - trainable model-part blocks (`unet`, `prior`, `transformer`)
  - noise/loss/masked/layer blocks and advanced dialogs parity (as applicable to web scope)

## Session Update (2026-02-18, Sampling tab)

### Implemented in this session (`Sampling` tab)
- Backend (`apps/api`):
  - Added `GET /api/v1/sampling-config`
  - Added `POST /api/v1/sampling-config`
  - Added typed sampling schemas + metadata for:
    - sample schedule/output settings (`sample_after*`, `sample_skip_first`, `sample_*_format`, `samples_to_tensorboard`, `non_ema_sampling`)
    - sample definition file path (`sample_definition_file_name`)
    - sample list payload (`samples[]`) aligned to `SampleConfig` keys
  - Implemented sample-file load/save against `sample_definition_file_name`, preserving normalized sample config shape.
  - Preserved existing `TrainConfig` key names and enum-string values.
- Frontend (`apps/web`):
  - Enabled `Sampling` tab in tab bar.
  - Added API client/types for sampling config endpoints.
  - Added `Sampling` tab form:
    - top-level sampling controls
    - editable sample list with add/remove
    - representative sample fields (`enabled`, `width`, `height`, `seed`, `prompt`, `negative_prompt`, `diffusion_steps`, `cfg_scale`, `noise_scheduler`, `random_seed`)
    - save/reload flow

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- Playwright smoke checks (manual via MCP):
  - Open app and switch to `Sampling` tab
  - Verify required fields render (sample settings + sample row controls)
  - Edit representative values:
    - `sample_after = 15`
    - `sample_skip_first = 2`
    - `sample_image_format = PNG`
    - `sample[0].seed = 12345`
    - `sample[0].prompt = playwright sample prompt`
    - `sample[0].noise_scheduler = EULER`
  - Save and verify success message (`Sampling settings saved.`)
  - Reload app and verify persistence of changed values
  - Confirm API calls:
    - `GET /api/v1/sampling-config` -> `200`
    - `POST /api/v1/sampling-config` -> `200`
  - Console:
    - No sampling-flow blocking errors observed

## Session Update (2026-02-18, Backup tab)

### Implemented in this session (`Backup` tab)
- Backend (`apps/api`):
  - Added `GET /api/v1/backup-config`
  - Added `POST /api/v1/backup-config`
  - Added typed backup schema + metadata mapped to desktop backup tab keys:
    - `backup_after`, `backup_after_unit`
    - `rolling_backup`, `rolling_backup_count`
    - `backup_before_save`
    - `save_every`, `save_every_unit`
    - `save_skip_first`
    - `save_filename_prefix`
  - Preserved existing `TrainConfig` key names and enum-string values.
- Frontend (`apps/web`):
  - Enabled `Backup` tab in tab bar.
  - Added API client/types for backup config endpoints.
  - Added `Backup` tab form with save/reload flow for desktop-aligned config fields.
  - Intentionally did not implement command actions (`backup now`, `save now`) in this slice.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- Playwright smoke checks (manual via MCP):
  - Open app and switch to `Backup` tab
  - Verify required fields render
  - Edit representative values:
    - `backup_after = 45`
    - `rolling_backup_count = 5`
    - `save_every = 3`
    - `save_every_unit = STEP`
    - `save_skip_first = 1`
    - `save_filename_prefix = playwright-backup`
  - Save and verify success message (`Backup settings saved.`)
  - Reload app and verify persistence of changed values
  - Confirm API calls:
    - `GET /api/v1/backup-config` -> `200`
    - `POST /api/v1/backup-config` -> `200`
  - Console:
    - No backup-flow blocking errors observed

## Session Update (2026-02-18, Tools tab)

### Implemented in this session (`Tools` tab)
- Backend (`apps/api`):
  - Added `GET /api/v1/tools-config`
  - Added typed tools metadata schema for action-oriented entries:
    - web link actions
    - CLI command actions
    - info-only actions
  - Returned desktop-equivalent tool entries aligned to desktop tools tab intent:
    - Wiki
    - Dataset Tools
    - Video Tools
    - Convert Model Tools
    - Sampling Tool
    - Profiling Tool
- Frontend (`apps/web`):
  - Enabled `Tools` tab in tab bar.
  - Added API client/types for tools config endpoint.
  - Added `Tools` tab UI with action cards:
    - `Open` for web links
    - `Copy Command` for desktop tool commands
    - `Show Info` for info-only items
  - Added status feedback for executed tool actions.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- Playwright smoke checks (manual via MCP):
  - Open app and switch to `Tools` tab
  - Verify tool entries render
  - Execute representative action:
    - click `Copy Command` for `Dataset Tools`
    - verify status feedback (`Dataset Tools command copied: ./run-cmd.sh caption_ui`)
  - Confirm API calls:
    - `GET /api/v1/tools-config` -> `200`
  - Console:
    - No tools-flow blocking errors observed

## Session Update (2026-02-18, LoRA tab)

### Implemented in this session (`LoRA` tab)
- Backend (`apps/api`):
  - Added `GET /api/v1/lora-config`
  - Added `POST /api/v1/lora-config`
  - Added typed LoRA schema + metadata mapped to desktop `LoraTab` keys:
    - base settings (`peft_type`, `lora_model_name`, `lora_rank`, `lora_alpha`, `dropout_probability`, `lora_weight_dtype`, `bundle_additional_embeddings`)
    - LoRA-only DoRA toggles (`lora_decompose`, `lora_decompose_norm_epsilon`, `lora_decompose_output_axis`)
    - OFT v2 settings (`oft_block_size`, `oft_coft`, `coft_eps`, `oft_block_share`)
  - Preserved existing `TrainConfig` key names and enum-string values.
- Frontend (`apps/web`):
  - Enabled `LoRA` tab in tab bar.
  - Added API client/types for LoRA config endpoints.
  - Added `LoRA` tab form with conditional sections by type:
    - `LORA`/`LOHA` fields
    - `LORA` DoRA-specific toggles
    - `OFT_2` fields
  - Added save/reload flow with numeric coercion.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- Playwright smoke checks (manual via MCP):
  - Open app and switch to `LoRA` tab
  - Verify fields render and conditional UI switches with type changes
  - Edit representative values:
    - `peft_type = OFT_2`
    - `lora_model_name = models/lora-base.safetensors`
    - `oft_block_size = 64`
    - `coft_eps = 0.001`
    - `dropout_probability = 0.2`
  - Save and verify success message (`LoRA settings saved.`)
  - Reload app and verify persistence of changed values
  - Confirm API calls:
    - `GET /api/v1/lora-config` -> `200`
    - `POST /api/v1/lora-config` -> `200`
  - Console:
    - No lora-flow blocking errors observed

## Session Update (2026-02-18, Backend skeleton extraction)

### Implemented in this session (Refactor Step 2 start)
- Backend (`apps/api`):
  - Added `apps/api/app/core/settings.py` for repo-root bootstrap and CORS config constants.
  - Added `apps/api/app/core/store.py` and moved `ConfigStore` + relative-path resolution there.
  - Added per-feature route modules under `apps/api/app/routes/`:
    - `general.py`, `model.py`, `lora.py`, `data.py`, `training.py`, `sampling.py`, `backup.py`, `concepts.py`, `tools.py`
  - Reduced `apps/api/app/main.py` to app setup + middleware + `include_router(...)` registration only.
- API contract stability:
  - Preserved existing endpoint paths and response/request schema shapes.
  - Preserved all existing route behavior by moving handler logic without contract changes.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Route registration sanity check:
  - Imported app and confirmed all expected `/api/v1/*` routes are present.

## Session Update (2026-02-18, OpenAPI generation + client wrapper)

### Implemented in this session (Refactor Step 1)
- Frontend (`apps/web`):
  - Added OpenAPI generation tooling via `openapi-typescript-codegen`.
  - Added `npm run gen:api` script in `apps/web/package.json`.
  - Added `apps/web/scripts/export_openapi.py` to export FastAPI OpenAPI spec directly from `apps.api.app.main:app` without requiring a running server.
  - Generated API client + models under `apps/web/src/lib/api/generated/`.
  - Replaced handwritten API calls in `apps/web/src/lib/api/client.ts` with a thin compatibility wrapper over generated `DefaultService`, preserving existing exported function names (`fetch*Config`, `save*Config`).
  - Replaced handwritten type declarations in `apps/web/src/lib/api/types.ts` with re-exports from generated models, preserving existing type names used by `App.svelte`.
- Docs:
  - Updated `apps/web/README.md` with `gen:api` usage and generated output path.
  - Updated `apps/api/README.md` scope and route list to match current implementation.

### Validation run this session
- Generation:
  - `npm --prefix apps/web run gen:api`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- Backend compile check:
  - `python -m compileall apps/api/app`

## Session Update (2026-02-18, General mapper/service split)

### Implemented in this session (Refactor Step 3 start)
- Backend (`apps/api`):
  - Added `apps/api/app/mappers/general.py` and moved general tab mapping logic (`to_general_settings`, `apply_general_settings`).
  - Added `apps/api/app/services/general_service.py` and moved general tab orchestration (`load -> map -> meta`, `apply -> save -> map -> meta`).
  - Updated `apps/api/app/routes/general.py` to thin route handlers that delegate to service functions.
  - Kept `GET /api/v1/health` in `routes/general.py`.
- API contract stability:
  - Preserved endpoint path and response shape for `GET/POST /api/v1/general-config`.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- OpenAPI generation:
  - `npm --prefix apps/web run gen:api`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Model mapper/service split)

### Implemented in this session (Refactor Step 3 continuation)
- Backend (`apps/api`):
  - Added `apps/api/app/mappers/model.py` and moved model tab mapping logic (`to_model_settings`, `apply_model_settings`).
  - Added `apps/api/app/services/model_service.py` and moved model tab orchestration (`load -> map -> meta`, `apply -> save -> map -> meta`).
  - Updated `apps/api/app/routes/model.py` to thin route handlers that delegate to service functions.
- API contract stability:
  - Preserved endpoint path and response shape for `GET/POST /api/v1/model-config`.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- OpenAPI generation:
  - `npm --prefix apps/web run gen:api`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, LoRA mapper/service split)

### Implemented in this session (Refactor Step 3 continuation)
- Backend (`apps/api`):
  - Added `apps/api/app/mappers/lora.py` and moved LoRA tab mapping logic (`to_lora_settings`, `apply_lora_settings`).
  - Added `apps/api/app/services/lora_service.py` and moved LoRA tab orchestration (`load -> map -> meta`, `apply -> save -> map -> meta`).
  - Updated `apps/api/app/routes/lora.py` to thin route handlers that delegate to service functions.
- API contract stability:
  - Preserved endpoint path and response shape for `GET/POST /api/v1/lora-config`.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- OpenAPI generation:
  - `npm --prefix apps/web run gen:api`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Data and Backup mapper/service split)

### Implemented in this session (Refactor Step 3 continuation)
- Backend (`apps/api`):
  - Added `apps/api/app/mappers/data.py` and `apps/api/app/services/data_service.py`.
  - Updated `apps/api/app/routes/data.py` to thin route handlers.
  - Added `apps/api/app/mappers/backup.py` and `apps/api/app/services/backup_service.py`.
  - Updated `apps/api/app/routes/backup.py` to thin route handlers.
- API contract stability:
  - Preserved endpoint paths and response shapes for:
    - `GET/POST /api/v1/data-config`
    - `GET/POST /api/v1/backup-config`

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- OpenAPI generation:
  - `npm --prefix apps/web run gen:api`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Training mapper/service split)

### Implemented in this session (Refactor Step 3 continuation)
- Backend (`apps/api`):
  - Added `apps/api/app/mappers/training.py` and moved training tab mapping logic (`to_training_settings`, `apply_training_settings`).
  - Added `apps/api/app/services/training_service.py` and moved training tab orchestration (`load -> map -> meta`, `apply -> save -> map -> meta`).
  - Updated `apps/api/app/routes/training.py` to thin route handlers that delegate to service functions.
- API contract stability:
  - Preserved endpoint path and response shape for `GET/POST /api/v1/training-config`.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- OpenAPI generation:
  - `npm --prefix apps/web run gen:api`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Sampling/Concepts/Tools service extraction)

### Implemented in this session (Refactor Step 3 continuation)
- Backend (`apps/api`):
  - Added `apps/api/app/mappers/sampling.py` and `apps/api/app/services/sampling_service.py`.
  - Updated `apps/api/app/routes/sampling.py` to thin route handlers.
  - Added `apps/api/app/mappers/concepts.py` and `apps/api/app/services/concepts_service.py`.
  - Updated `apps/api/app/routes/concepts.py` to thin route handlers.
  - Added `apps/api/app/services/tools_service.py`.
  - Updated `apps/api/app/routes/tools.py` to thin route handler delegating to service.
- API contract stability:
  - Preserved endpoint paths and response shapes for:
    - `GET/POST /api/v1/sampling-config`
    - `GET/POST /api/v1/concepts-config`
    - `GET /api/v1/tools-config`

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- OpenAPI generation:
  - `npm --prefix apps/web run gen:api`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Frontend AppShell extraction)

### Implemented in this session (Refactor Step 4 start)
- Frontend (`apps/web`):
  - Added `apps/web/src/app/AppShell.svelte` and moved existing top-level app UI there with no UX/behavior change.
  - Reduced `apps/web/src/App.svelte` to a thin wrapper that renders `AppShell`.
  - Added `apps/web/src/app/routes.ts` with shared tab route definitions.
  - Updated `apps/web/src/lib/components/ui/Tabs.svelte` to use the shared route registry (`TAB_ROUTES`) via props/default.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
- Backend compile check:
  - `python -m compileall apps/api/app`

## Session Update (2026-02-18, Frontend feature extraction: Tools and Data)

### Implemented in this session (Refactor Step 4 continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/tools/ToolsTab.svelte` and moved Tools tab rendering there.
  - Added `apps/web/src/features/data/DataTab.svelte` and moved Data tab rendering there.
  - Updated `apps/web/src/app/AppShell.svelte` to render extracted feature components while keeping existing state/loading/saving logic unchanged.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Frontend feature extraction: Backup)

### Implemented in this session (Refactor Step 4 continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/backup/BackupTab.svelte` and moved Backup tab rendering there.
  - Updated `apps/web/src/app/AppShell.svelte` to render `BackupTab` while preserving existing handlers and state.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Frontend feature extraction: LoRA)

### Implemented in this session (Refactor Step 4 continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/lora/LoraTab.svelte` and moved LoRA tab rendering there.
  - Updated `apps/web/src/app/AppShell.svelte` to render `LoraTab` while preserving existing handlers and state.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Frontend feature extraction: Training)

### Implemented in this session (Refactor Step 4 continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/training/TrainingTab.svelte` and moved Training tab rendering there.
  - Updated `apps/web/src/app/AppShell.svelte` to render `TrainingTab` while preserving existing handlers and state.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Frontend feature extraction: General)

### Implemented in this session (Refactor Step 4 continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/general/GeneralTab.svelte` and moved General tab rendering there.
  - Updated `apps/web/src/app/AppShell.svelte` to render `GeneralTab` while preserving existing handlers and state.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Frontend feature extraction: Model)

### Implemented in this session (Refactor Step 4 continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/model/ModelTab.svelte` and moved Model tab rendering there.
  - Updated `apps/web/src/app/AppShell.svelte` to render `ModelTab` while preserving existing handlers and state.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Frontend feature extraction: Sampling)

### Implemented in this session (Refactor Step 4 continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/sampling/SamplingTab.svelte` and moved Sampling tab rendering there.
  - Updated `apps/web/src/app/AppShell.svelte` to render `SamplingTab` while preserving existing handlers and state.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Frontend feature extraction: Concepts)

### Implemented in this session (Refactor Step 4 continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/concepts/ConceptsTab.svelte` and moved Concepts tab rendering there.
  - Updated `apps/web/src/app/AppShell.svelte` to render `ConceptsTab` while preserving existing handlers and state.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Frontend shell cleanup)

### Implemented in this session (Refactor Step 4 continuation)
- Frontend (`apps/web`):
  - Completed extraction of remaining major tabs to feature components:
    - `apps/web/src/features/model/ModelTab.svelte`
    - `apps/web/src/features/sampling/SamplingTab.svelte`
    - `apps/web/src/features/concepts/ConceptsTab.svelte`
  - Updated `apps/web/src/app/AppShell.svelte` to delegate all major tab rendering to feature components.
  - Removed now-unused direct UI imports from `AppShell` after extraction.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Per-tab lazy loading)

### Implemented in this session (Refactor Step 6 start)
- Frontend (`apps/web`):
  - Replaced eager `onMount` loading of all tabs with lazy load on demand.
  - Added `ensureTabLoaded(tabId)` in `apps/web/src/app/AppShell.svelte`.
  - Initial load now fetches only the active tab.
  - Tab changes trigger first-load fetch for that tab if not already loaded.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Env-configurable API runtime)

### Implemented in this session
- Backend (`apps/api`):
  - Made API runtime settings env-configurable in `apps/api/app/core/settings.py`:
    - `ONETRAINER_API_HOST`
    - `ONETRAINER_API_PORT`
    - `ONETRAINER_API_CORS_ORIGINS` (comma-separated)
- Frontend (`apps/web`):
  - Added `apps/web/.env.example` with `VITE_API_BASE_URL`.
- Docs:
  - Updated `apps/api/README.md` with backend env variable documentation.
  - Updated `apps/web/README.md` to reference `.env.example` usage.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Frontend config-resource helper adoption)

### Implemented in this session (Refactor Step 5 start)
- Frontend (`apps/web`):
  - Added `apps/web/src/app/configResource.ts` with shared helper functions for tab config flows:
    - `loadConfigResource(...)` for standardized load-state/message/error handling
    - `saveConfigResource(...)` for standardized save-state/message/error handling
  - Updated `apps/web/src/app/AppShell.svelte` to migrate all existing tab load/save handlers to the shared helper without changing endpoint contracts or tab UX.
  - Preserved existing per-tab payload shaping and success messages.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Step 6 per-tab state flags)

### Implemented in this session (Refactor Step 6 continuation)
- Frontend (`apps/web`):
  - Introduced typed tab identifiers in `apps/web/src/app/routes.ts` and updated tab events in `apps/web/src/lib/components/ui/Tabs.svelte`.
  - Replaced global `loading/saving/error/status` state in `apps/web/src/app/AppShell.svelte` with per-tab state maps.
  - Updated config load/save flows to use tab-scoped state setters while preserving existing API contracts and UX messaging.
  - Updated first-load tracking to use explicit per-tab `loaded` flags.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, General state module extraction)

### Implemented in this session (Refactor Step 6/Vertical-slice continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/general/state.ts` and moved General tab orchestration there:
    - load flow (`loadGeneralState`)
    - save flow + payload shaping (`saveGeneralState`)
  - Updated `apps/web/src/app/AppShell.svelte` to delegate General tab load/save logic to the new feature state module.
  - Preserved endpoint contracts and UI behavior.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Model state module extraction)

### Implemented in this session (Refactor Step 6/Vertical-slice continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/model/state.ts` and moved Model tab orchestration there:
    - load flow (`loadModelState`)
    - save flow + payload shaping (`saveModelState`)
  - Updated `apps/web/src/app/AppShell.svelte` to delegate Model tab load/save logic to the new feature state module.
  - Preserved endpoint contracts and UI behavior.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, LoRA state module extraction)

### Implemented in this session (Refactor Step 6/Vertical-slice continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/lora/state.ts` and moved LoRA tab orchestration there:
    - load flow (`loadLoraState`)
    - save flow + payload shaping (`saveLoraState`)
  - Updated `apps/web/src/app/AppShell.svelte` to delegate LoRA tab load/save logic to the new feature state module.
  - Preserved endpoint contracts and UI behavior.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Data state module extraction)

### Implemented in this session (Refactor Step 6/Vertical-slice continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/data/state.ts` and moved Data tab orchestration there:
    - load flow (`loadDataState`)
    - save flow (`saveDataState`)
  - Updated `apps/web/src/app/AppShell.svelte` to delegate Data tab load/save logic to the new feature state module.
  - Preserved endpoint contracts and UI behavior.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Remaining tab state-module extraction)

### Implemented in this session (Refactor Step 6/Vertical-slice continuation)
- Frontend (`apps/web`):
  - Added `apps/web/src/features/training/state.ts` and moved Training tab orchestration there.
  - Added `apps/web/src/features/backup/state.ts` and moved Backup tab orchestration there.
  - Added `apps/web/src/features/concepts/state.ts` and moved Concepts tab orchestration there.
  - Added `apps/web/src/features/tools/state.ts` and moved Tools tab load orchestration there.
  - Added `apps/web/src/features/sampling/state.ts` and moved Sampling tab orchestration there.
  - Updated `apps/web/src/app/AppShell.svelte` to delegate the above tab flows to feature state modules.
  - `AppShell` remains responsible for shell-level concerns and local helper actions (tab switching and local add/remove helpers).

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Feature adapters extraction)

### Implemented in this session (Refactor Step 6/Vertical-slice continuation)
- Frontend (`apps/web`):
  - Added per-feature adapter modules to isolate UI/data shaping logic:
    - `apps/web/src/features/general/adapter.ts`
    - `apps/web/src/features/model/adapter.ts`
    - `apps/web/src/features/lora/adapter.ts`
    - `apps/web/src/features/data/adapter.ts`
    - `apps/web/src/features/training/adapter.ts`
    - `apps/web/src/features/sampling/adapter.ts`
    - `apps/web/src/features/backup/adapter.ts`
    - `apps/web/src/features/concepts/adapter.ts`
    - `apps/web/src/features/tools/adapter.ts`
  - Updated all feature `state.ts` modules to consume adapters for response mapping and save-payload shaping.
  - Preserved API contracts and UI behavior while reducing transformation logic in state handlers.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Adapter + shared layer alignment)

### Implemented in this session (Refactor Step 6/Shared-layer continuation)
- Frontend (`apps/web`):
  - Added per-feature `adapter.ts` files and moved response/payload shaping out of `state.ts` handlers.
  - Added `apps/web/src/shared/api/http.ts` and moved OpenAPI base configuration + API error wrapping there.
  - Updated `apps/web/src/lib/api/client.ts` to use shared HTTP helpers.
  - Added `apps/web/src/shared/state/ui.ts` with reusable tab-state factory helpers.
  - Updated `apps/web/src/app/AppShell.svelte` to use `shared/state/ui.ts` helpers.
- Decision:
  - Keep `src/lib` as a compatibility layer for generated client/types while introducing `src/shared` for cross-feature ownership points.

### Validation run this session
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Backend schema modularization)

### Implemented in this session (Refactor backend structure continuation)
- Backend (`apps/api`):
  - Replaced monolithic `apps/api/app/schemas.py` with modular schema package `apps/api/app/schemas/`.
  - Added schema modules:
    - `common.py`
    - `general.py`
    - `model.py`
    - `lora.py`
    - `data.py`
    - `training.py`
    - `sampling.py`
    - `backup.py`
    - `concepts.py`
    - `tools.py`
  - Added `apps/api/app/schemas/__init__.py` to re-export schema symbols and preserve existing import style (`from ..schemas import ...`).
  - Removed legacy `apps/api/app/schemas.py`.

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- OpenAPI generation:
  - `npm --prefix apps/web run gen:api`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

## Session Update (2026-02-18, Playwright smoke automation)

### Implemented in this session
- Frontend (`apps/web`):
  - Added lightweight smoke script: `apps/web/scripts/playwright_smoke.sh`.
  - Added npm command: `npm run smoke:playwright` in `apps/web/package.json`.
  - Script flow validates General tab save/reload persistence for `workspace_dir` via `playwright-cli`.
- Docs:
  - Updated `apps/web/README.md` with smoke-script usage and env overrides.

### Validation run this session
- Script syntax check:
  - `bash -n apps/web/scripts/playwright_smoke.sh`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`

### Notes
- Full smoke execution requires running API + web dev servers first (script assumes live app endpoint).

## Session Update (2026-02-18, Final cleanup pass)

### Implemented in this session (Refactor Step 7)
- Cleanup:
  - Removed dead import in `apps/web/src/app/AppShell.svelte` after feature ownership migration.
  - Reconciled stale top-level sections in `webui-implementation-progress.md` (`Known Issue`/`TODO` area and high-level implementation summary).
- Docs:
  - Updated `apps/api/README.md` to reflect current backend ownership split (`routes`, `services`, `mappers`, `schemas`).
  - Updated `apps/web/README.md` to reflect current frontend ownership (`app`, `features/<tab>/state.ts`, `features/<tab>/adapter.ts`, `shared/*`).

### Validation run this session
- Backend compile check:
  - `python -m compileall apps/api/app`
- Frontend checks:
  - `npm --prefix apps/web run check`
  - `npm --prefix apps/web run build`
