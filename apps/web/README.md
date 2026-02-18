# OneTrainer Web UI

Svelte frontend for the OneTrainer web migration.

## Run

```bash
cd apps/web
npm install
npm run gen:api
npm run dev
```

Optional API override:

```bash
VITE_API_BASE_URL=http://localhost:8011 npm run dev
```

Or copy the example env file:

```bash
cp .env.example .env
```

## Scope

Current UI includes `General`, `Model`, `LoRA`, `Data`, `Training`, `Sampling`, `Backup`, `Tools`, and `Concepts`.

Architecture status:
- Shell/layout and tab switching in `src/app/AppShell.svelte`
- Tab registry in `src/app/routes.ts`
- Per-feature UI in `src/features/<tab>/<Tab>.svelte`
- Per-feature orchestration in `src/features/<tab>/state.ts`
- Per-feature data shaping in `src/features/<tab>/adapter.ts`
- Shared HTTP/state helpers in `src/shared/*`
- Generated OpenAPI client/types in `src/lib/api/generated/*` (kept as compatibility layer)

## API Client Generation

OpenAPI client/types are generated from the local FastAPI app contract:

```bash
cd apps/web
npm run gen:api
```

Generated files are written to `src/lib/api/generated/`.

## Playwright Smoke

With API + web dev servers running, execute:

```bash
cd apps/web
npm run smoke:playwright
```

Optional overrides:
- `WEB_UI_URL` (default: `http://127.0.0.1:5173`)
- `PLAYWRIGHT_SMOKE_SESSION` (custom playwright-cli session name)
