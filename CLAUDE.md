# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OneTrainer is a modular training framework for diffusion models (Stable Diffusion 1.5/2/3/XL, FLUX.1/2, PixArt, Sana, Hunyuan Video, Chroma, HiDream, etc.). It supports fine-tuning, LoRA, embeddings, and VAE training via both a CustomTkinter GUI and CLI scripts.

## Build & Development Commands

```bash
# Install dependencies (uses uv package manager)
./install.sh          # Linux/macOS
install.bat           # Windows

# Update project + dependencies
./update.sh

# Launch GUI
./start-ui.sh

# Run CLI scripts through wrapper
./run-cmd.sh train -h
./run-cmd.sh sample -h
./run-cmd.sh convert_model -h

# Linting (Ruff - enforced via pre-commit)
pre-commit run --all-files

# Install dev tooling
pip install -r requirements-dev.txt && pre-commit install
```

There is no test suite. Validation is done via pre-commit (Ruff) and manual smoke tests (`./run-cmd.sh train -h`, `./run-cmd.sh sample -h`). For training/data-path changes, validate with a preset from `training_presets/`.

## Architecture

### Factory-based Plugin System

The core pattern is a **registry-based factory** (`modules/util/factory.py`). Implementations register themselves on import, and `create.py` resolves them by `(ModelType, TrainingMethod)` tuples:

```python
# In a module file (e.g. modules/modelLoader/FluxLoRAModelLoader.py):
factory.register(BaseModelLoader, FluxLoRAModelLoader, ModelType.FLUX_DEV_1, TrainingMethod.LORA)

# At startup, create.py auto-imports all implementations:
factory.import_dir("modules/modelLoader", "modules.modelLoader")

# Resolution:
loader_cls = factory.get(BaseModelLoader, model_type, training_method)
```

### Core Abstractions

Each model type provides implementations of these base classes, resolved via the factory by `(ModelType, TrainingMethod)`:

| Base Class | Role | Location |
|---|---|---|
| `BaseModel` | Holds all model components (tokenizer, text encoder, VAE, UNet/transformer, LoRA adapters) | `modules/model/` |
| `BaseModelLoader` | Loads model from disk (diffusers, ckpt, safetensors) | `modules/modelLoader/` |
| `BaseModelSetup` | Configures training: creates parameter groups, sets up optimizations, defines `predict()` and `calculate_loss()` | `modules/modelSetup/` |
| `BaseModelSampler` | Generates inference samples during training | `modules/modelSampler/` |
| `BaseModelSaver` | Saves trained model to disk | `modules/modelSaver/` |
| `BaseDataLoader` | Creates MGDS graph-based dataset with caching/augmentation | `modules/dataLoader/` |

### Training Flow

1. **Config** (`TrainConfig` in `modules/util/config/TrainConfig.py`) — 200+ parameters serialized as JSON
2. **Trainer** (`GenericTrainer` in `modules/trainer/GenericTrainer.py`) orchestrates the pipeline:
   - `start()`: ModelLoader → BaseModel → ModelSetup → DataLoader
   - `train()`: epoch loop → batch → `ModelSetup.predict()` → `calculate_loss()` → backward → optimizer step
   - `end()`: ModelSaver → disk
3. **UI↔Trainer coupling** via `TrainCallbacks` (events: progress, status) and `TrainCommands` (queue: sample, backup, save, stop)

### Key Directories

- `modules/model/` — Model data classes (one per architecture)
- `modules/modelLoader/`, `modelSetup/`, `modelSampler/`, `modelSaver/` — Per-model implementations
- `modules/dataLoader/` — MGDS-based data pipelines
- `modules/trainer/` — `GenericTrainer` (main loop), `CloudTrainer`, `MultiTrainer`
- `modules/module/` — Training technique implementations (LoRA, EMA, OFT, embeddings)
- `modules/ui/` — CustomTkinter GUI components
- `modules/util/config/` — Configuration classes (`TrainConfig`, `ConceptConfig`, etc.)
- `modules/util/enum/` — 27 enum types (`ModelType`, `TrainingMethod`, `Optimizer`, `DataType`, etc.)
- `modules/util/create.py` — Factory resolution + optimizer/scheduler creation
- `scripts/` — Thin entry-point wrappers (keep logic in `modules/`)

### Adding a New Model

Follow the existing pattern: create implementations of `BaseModel`, `BaseModelLoader`, `BaseModelSetup`, `BaseModelSampler`, `BaseModelSaver`, and `BaseDataLoader`, each registering via `factory.register()` with the new `ModelType` enum value. Name classes to match existing conventions (e.g., `Flux2LoRAModelLoader`).

## Code Style

- **Ruff** with 120-char line length, double quotes, 4-space indent
- **Import order**: future → stdlib → first-party → mgds → torch → hf (huggingface) → third-party → local (custom isort sections in `pyproject.toml`)
- **Naming**: `snake_case` functions/files, `PascalCase` classes, aligned with module families (`StableDiffusion...`, `Flux...`, `...ModelLoader`)
- **Line endings**: LF (CRLF only for `.bat` files)

## Commit Conventions

- Imperative subjects: "Fix Model Conversion Tool", "Add Flux2 support"
- Reference issues/PRs: `(#1319)`
- PRs include: purpose, scope, affected modules, validation steps, and UI screenshots when applicable
