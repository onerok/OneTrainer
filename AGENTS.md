# Repository Guidelines

## Project Structure & Module Organization
- Core application code lives in `modules/`, organized by responsibility (`model/`, `modelLoader/`, `modelSetup/`, `trainer/`, `ui/`, `util/`, etc.).
- User-facing entry points are in `scripts/` (for example `train.py`, `sample.py`, `convert_model.py`, `generate_captions.py`). Keep script logic thin and reusable logic in `modules/`.
- Static/runtime data is stored in `resources/` (model specs, configs, docker files, icons), with reusable presets in `training_presets/` and prompt templates in `embedding_templates/`.
- Architecture and onboarding docs are in `docs/` (`ProjectStructure.md`, `QuickStartGuide.md`, `CliTraining.md`).

## Build, Test, and Development Commands
- Install dependencies: `./install.sh` (Linux/macOS) or `install.bat` (Windows).
- Update project + dependencies: `./update.sh` or `update.bat`.
- Launch GUI: `./start-ui.sh` or `start-ui.bat`.
- Run CLI tasks safely through wrapper: `./run-cmd.sh <script> [args]`.
  - Example: `./run-cmd.sh train -h`
- Install contributor tooling: `pip install -r requirements-dev.txt && pre-commit install`.
- Run quality checks locally: `pre-commit run --all-files`.

## Coding Style & Naming Conventions
- Python style is enforced by Ruff (`pyproject.toml`) with a 120-char line length.
- `.editorconfig` rules: UTF-8, LF endings, 4-space indentation (CRLF for `*.bat`).
- Use `snake_case` for functions/files, `PascalCase` for classes, and keep naming aligned with existing module families (for example `StableDiffusion...`, `Flux...`, `...ModelLoader`).
- Prefer explicit typing/config structures already used in `modules/util/config/` and related enums.

## Testing Guidelines
- There is currently no dedicated `tests/` suite in this repository.
- Before opening a PR, run `pre-commit run --all-files` and perform targeted CLI smoke checks:
  - `./run-cmd.sh train -h`
  - `./run-cmd.sh sample -h`
- For training/data-path changes, validate with a relevant preset from `training_presets/` and include the exact command used.

## Commit & Pull Request Guidelines
- Follow concise, imperative commit subjects (for example `Fix Model Conversion Tool`, `Update adv_optm version...`).
- Keep commits focused; reference issues/PRs when applicable (for example `(#1319)`).
- PRs should include: purpose, scope, affected modules/scripts, validation steps, and any UI screenshots/log snippets when behavior changes.
- For larger features, start with a Discussion/Discord alignment before implementation.
