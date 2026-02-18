# OneTrainer Web API

FastAPI backend for the new web UI.

## Run

```bash
cd apps/api
uv sync
uv run uvicorn app.main:app --reload --port 8011
```

## Scope

Implements web-config endpoints for `General`, `Model`, `LoRA`, `Data`, `Training`, `Sampling`, `Backup`, `Tools`, and `Concepts`.

Current routes:
- `GET/POST /api/v1/general-config`
- `GET/POST /api/v1/model-config`
- `GET/POST /api/v1/lora-config`
- `GET/POST /api/v1/data-config`
- `GET/POST /api/v1/training-config`
- `GET/POST /api/v1/sampling-config`
- `GET/POST /api/v1/backup-config`
- `GET/POST /api/v1/concepts-config`
- `GET /api/v1/tools-config`
- `GET /api/v1/health`

Config is persisted to `training_user_settings/web-general-config.json`.
