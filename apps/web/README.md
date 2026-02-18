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

## API Client Generation

OpenAPI client/types are generated from the local FastAPI app contract:

```bash
cd apps/web
npm run gen:api
```

Generated files are written to `src/lib/api/generated/`.
