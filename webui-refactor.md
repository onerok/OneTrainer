# WebUI Refactor Plan

## Goal
Refactor the WebUI/API architecture to vertical slices with minimal churn, while continuing tab-by-tab delivery.

## Target Folder Layout

### Backend (`apps/api/app`)
- `main.py` (app creation + router registration only)
- `core/`
- `core/settings.py` (env/CORS/runtime config)
- `core/store.py` (`ConfigStore`, file I/O helpers)
- `schemas/`
- `schemas/common.py` (shared enums/base models)
- `schemas/general.py`
- `schemas/model.py`
- `schemas/lora.py`
- `schemas/data.py`
- `schemas/training.py`
- `schemas/sampling.py`
- `schemas/backup.py`
- `schemas/concepts.py`
- `schemas/tools.py`
- `mappers/`
- `mappers/general.py`
- `mappers/model.py`
- `mappers/lora.py`
- `mappers/data.py`
- `mappers/training.py`
- `mappers/sampling.py`
- `mappers/backup.py`
- `mappers/concepts.py`
- `services/`
- `services/general_service.py`
- `services/model_service.py`
- `services/lora_service.py`
- `services/data_service.py`
- `services/training_service.py`
- `services/sampling_service.py`
- `services/backup_service.py`
- `services/concepts_service.py`
- `services/tools_service.py`
- `routes/`
- `routes/general.py`
- `routes/model.py`
- `routes/lora.py`
- `routes/data.py`
- `routes/training.py`
- `routes/sampling.py`
- `routes/backup.py`
- `routes/concepts.py`
- `routes/tools.py`

### Frontend (`apps/web/src`)
- `app/`
- `app/AppShell.svelte` (layout + tabs + status)
- `app/routes.ts` (tab registry)
- `shared/`
- `shared/api/http.ts` (base fetch/error wrapper)
- `shared/api/generated/` (OpenAPI-generated client + types)
- `shared/state/ui.ts` (global non-tab UI state only)
- `shared/components/ui/*` (existing)
- `features/`
- `features/general/GeneralTab.svelte`
- `features/general/state.ts`
- `features/general/adapter.ts` (if needed for UI-only shaping)
- same pattern for `model`, `lora`, `data`, `training`, `sampling`, `backup`, `concepts`, `tools`

## Refactor Sequence (Minimize Churn)

### 1. Stabilize Contracts First
- Keep all existing endpoint paths and response shapes unchanged.
- Add OpenAPI generation in web build (`npm run gen:api`) and commit generated client/types.
- Switch `client.ts` callers to generated client through a thin compatibility wrapper.

### 2. Backend Skeleton Extraction (No Behavior Change)
- Create `core/store.py` and move `ConfigStore` + path helpers.
- Move each tab’s GET/POST handlers into `routes/<tab>.py` with same bodies initially.
- Keep `main.py` limited to app setup, middleware, and `include_router(...)`.

### 3. Mapper/Service Split Per Tab
- Start with `general`.
- Move `_to_*` / `_apply_*` logic into `mappers/general.py`.
- Move orchestration/load-save/meta assembly into `services/general_service.py`.
- Keep route thin: call service only.
- Repeat tab-by-tab.

### 4. Frontend Shell Split (No UX Change)
- Create `AppShell.svelte`; move tabs + top-level status/messages there.
- Extract each tab block from `App.svelte` into `features/<tab>/<Tab>.svelte` incrementally.
- Keep current props/events first (no store rewrite yet).

### 5. Introduce Generic Config-Resource Helper
- Add shared helper for `load/save/error/meta`.
- Migrate each feature to helper gradually.
- Remove duplicated tab-level fetch/save boilerplate as each feature migrates.

### 6. Per-Tab Lazy Load + Per-Tab Flags
- Add per-feature `loaded/loading/saving/error` state.
- Load on first tab activation, not global app mount.
- Keep explicit per-tab `Reload`.

### 7. Cleanup Phase
- Remove handwritten duplicated API types once generated types fully adopted.
- Delete dead logic from legacy `App.svelte`.
- Update docs:
- `apps/api/README.md`
- `apps/web/README.md`
- `webui-implementation-progress.md`

## Recommended PR Cadence

1. PR1: OpenAPI generation + client wrapper, zero behavior change.
2. PR2: Backend route/store extraction, zero behavior change.
3. PR3+: One tab per PR full slice (`route + service + mapper + feature component + resource helper adoption`).
4. Final PR: lazy loading and legacy cleanup.
