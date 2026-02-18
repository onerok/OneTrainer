# OneTrainer justfile
# https://github.com/casey/just

set shell := ["bash", "-uc"]
set dotenv-load := true

# Platform group: "detect" (default), "cuda", "rocm", or "cpu"
platform := env("OT_PLATFORM_REQUIREMENTS", "detect")

# Disable buggy Xet by default
export HF_HUB_DISABLE_XET := env("HF_HUB_DISABLE_XET", "1")

# List available recipes
default:
    @just --list

# Install/sync dependencies (auto-detects GPU platform)
install:
    ./install.sh

# Update project and dependencies from git
update:
    ./update.sh

# Launch the training GUI
ui:
    ./start-ui.sh

# Run a CLI script (e.g., just run train --help)
run script *ARGS:
    ./run-cmd.sh {{ script }} {{ ARGS }}

# Train a model from a config file
train config *ARGS:
    ./run-cmd.sh train --config-path {{ config }} {{ ARGS }}

# Generate samples from a config file
sample config *ARGS:
    ./run-cmd.sh sample --config-path {{ config }} {{ ARGS }}

# Convert a model between formats
convert *ARGS:
    ./run-cmd.sh convert_model {{ ARGS }}

# Generate captions for images
captions *ARGS:
    ./run-cmd.sh generate_captions {{ ARGS }}

# Generate masks for images
masks *ARGS:
    ./run-cmd.sh generate_masks {{ ARGS }}

# Calculate loss for a config
loss config *ARGS:
    ./run-cmd.sh calculate_loss --config-path {{ config }} {{ ARGS }}

# Launch the caption editor UI
caption-ui:
    ./run-cmd.sh caption_ui

# Launch the model converter UI
convert-ui:
    ./run-cmd.sh convert_model_ui

# Launch the video tool UI
video-ui:
    ./run-cmd.sh video_tool_ui

# Run ruff linter
lint:
    pre-commit run ruff-lint --all-files

# Run ruff formatter check
format-check:
    pre-commit run ruff-format --all-files

# Format code with ruff
format:
    uv run ruff format .

# Run all pre-commit hooks
check:
    pre-commit run --all-files

# Install dev tooling (pre-commit hooks)
dev-setup:
    uv sync --group dev && pre-commit install

# List available training presets
presets:
    @ls -1 training_presets/*.json | sed 's|training_presets/||; s|\.json$||'

# Generate a debug report
debug-report:
    ./run-cmd.sh generate_debug_report

# Run web API + web UI in one tmux session (detach with Ctrl-b d)
web-tmux session="onetrainer-web":
    @if ! command -v tmux >/dev/null 2>&1; then \
        echo "tmux is required but not installed."; \
        exit 1; \
    fi
    @if tmux has-session -t {{session}} 2>/dev/null; then \
        echo "Attaching to existing tmux session: {{session}}"; \
        tmux attach -t {{session}}; \
    else \
        tmux new-session -d -s {{session}} -n dev "cd apps/api && uv sync && uv run uvicorn app.main:app --reload --port 8011"; \
        tmux split-window -h -t {{session}}:dev "cd apps/web && npm install && npm run dev"; \
        tmux set-option -t {{session}}:dev remain-on-exit on; \
        tmux select-layout -t {{session}}:dev even-horizontal; \
        echo "Created tmux session: {{session}}"; \
        tmux attach -t {{session}}; \
    fi
