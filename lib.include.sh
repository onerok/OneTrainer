#!/usr/bin/env bash

set -e

# Detect absolute path to the directory where "lib.include.sh" resides.
export SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Guard against including the library multiple times.
readonly SCRIPT_DIR

# Ensure that all scripts change their working dir to the root of the project.
cd -- "${SCRIPT_DIR}"

# User-configurable environment variables.
# IMPORTANT: Don't modify the code below! Pass these variables via the environment!
# - OT_PLATFORM_REQUIREMENTS: "detect" (default), "cuda", "rocm", or "cpu".
# - OT_LAZY_UPDATES: "true" to skip re-syncing when git hash is unchanged.
# - OT_CUDA_LOWMEM_MODE: "true" to reduce CUDA out-of-memory situations.
# - OT_SCRIPT_DEBUG: "true" to enable debug logging.
export OT_LAZY_UPDATES="${OT_LAZY_UPDATES:-false}"
export OT_CUDA_LOWMEM_MODE="${OT_CUDA_LOWMEM_MODE:-false}"
export OT_PLATFORM_REQUIREMENTS="${OT_PLATFORM_REQUIREMENTS:-detect}"
export OT_SCRIPT_DEBUG="${OT_SCRIPT_DEBUG:-false}"

# Internal environment variables.
export OT_UPDATE_METADATA_FILE="${SCRIPT_DIR}/update.var"
export OT_HOST_OS="$(uname -s)"

# Force PyTorch to use fallbacks on Mac systems.
if [[ "${OT_HOST_OS}" == "Darwin" ]]; then
    export PYTORCH_ENABLE_MPS_FALLBACK="1"
fi

# Change PyTorch memory allocation to reduce CUDA out-of-memory situations.
if [[ "${OT_CUDA_LOWMEM_MODE}" == "true" ]]; then
    export PYTORCH_CUDA_ALLOC_CONF="garbage_collection_threshold:0.6,max_split_size_mb:128"
fi

# Utility functions.
function escape_shell_command {
    # NOTE: "%q" ensures shell-compatible argument escaping.
    printf " %q" "$@" | sed 's/^ //'
}

function print {
    # NOTE: "%b" parses escape-sequences, allowing us to output "\n" newlines.
    printf "[OneTrainer] %b\n" "$*"
}

function print_warning {
    printf "[OneTrainer] Warning: %b\n" "$*" >&2
}

function print_error {
    printf "[OneTrainer] Error: %b\n" "$*" >&2
}

function print_debug {
    if [[ "${OT_SCRIPT_DEBUG}" == "true" ]]; then
        print "Debug: $*"
    fi
}

function print_command {
    # NOTE: "%s" prints the escaped command as-is without parsing escape-seqs.
    printf "[OneTrainer] + %s\n" "$(escape_shell_command "$@")"
}

# Checks if a command exists and is executable.
function can_exec {
    if [[ -z "$1" ]]; then
        print_error "can_exec requires 1 argument."
        return 1
    fi

    if local full_path="$(command -v "$1" 2>/dev/null)"; then
        if [[ ! -z "${full_path}" ]] && [[ -x "${full_path}" ]]; then
            return 0
        fi
    fi

    return 1
}

# Executes a shell command and displays the exact command for logging purposes.
function run_cmd {
    print_command "$@"
    "$@"
}

# Retrieves the most recent Git commit's hash.
function get_current_git_hash {
    # NOTE: Will not detect local code changes, only the newest commit's hash.
    git rev-parse HEAD
}

# Writes update-check metadata to disk.
function save_update_metadata {
    get_current_git_hash >"${OT_UPDATE_METADATA_FILE}"
}

# Checks whether the current Git state matches the last-seen metadata state.
function is_update_metadata_changed {
    if [[ -f "${OT_UPDATE_METADATA_FILE}" ]]; then
        local saved_hash="$(<"${OT_UPDATE_METADATA_FILE}")"
        local current_hash="$(get_current_git_hash)"
        print_debug "Saved Metadata Hash=\"${saved_hash}\", Current Hash=\"${current_hash}\""
        if [[ "${saved_hash}" == "${current_hash}" ]]; then
            # Signal "failure", meaning "metadata is NOT outdated, abort".
            return 1
        fi
    fi

    return 0
}

# Ensures that uv is installed and available.
function exit_if_no_uv {
    if ! can_exec uv; then
        print_error "uv is not installed or not in PATH."
        print "Install uv via: curl -LsSf https://astral.sh/uv/install.sh | sh"
        print "See: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
}

# Determines which dependency group to use based on available GPU hardware.
function get_platform_group {
    local platform="${OT_PLATFORM_REQUIREMENTS}"

    if [[ "${platform}" == "detect" ]]; then
        # NOTE: We MUST prioritize NVIDIA first, since machines that contain
        # *both* AMD and NVIDIA GPUs are usually running integrated AMD graphics
        # that's built into their CPU, whereas their *dedicated* GPU is NVIDIA.
        if [[ -e "/dev/nvidia0" ]] || can_exec nvidia-smi || can_exec "/usr/lib/wsl/lib/nvidia-smi"; then
            # NVIDIA graphics.
            #  "/dev/nvidia0": The "first" detected NVIDIA GPU in the system.
            #  "nvidia-smi": Driver tool for all NVIDIA GPUs made after 2010.
            #  "/usr/lib/wsl/lib/nvidia-smi": WSL's NVIDIA path (isn't in $PATH).
            # SEE: https://docs.nvidia.com/cuda/wsl-user-guide/
            platform="cuda"
        elif [[ -e "/dev/kfd" ]]; then
            # AMD graphics.
            platform="rocm"
        else
            # No GPU acceleration.
            platform="cpu"
        fi
    fi

    # Support legacy file-based values for backward compatibility.
    case "${platform}" in
        requirements-cuda.txt) platform="cuda" ;;
        requirements-rocm.txt) platform="rocm" ;;
        requirements-default.txt) platform="cpu" ;;
    esac

    echo "${platform}"
}

# Syncs the uv environment with the detected platform group.
function sync_environment {
    local group="$(get_platform_group)"
    print "Syncing environment for platform: ${group}..."
    run_cmd uv sync --group "${group}"
}

# Runs a Python command within the uv-managed environment.
function run_python {
    local group="$(get_platform_group)"
    run_cmd uv run --group "${group}" python "$@"
}

# Performs the most important startup sanity checks and environment preparation.
function prepare_runtime_environment {
    # Ensure that uv is installed.
    exit_if_no_uv

    # Determine whether to sync dependencies.
    # NOTE: If "OT_LAZY_UPDATES" is "true", we will check the last update status
    # to determine if the source code has changed since our previous sync.
    # This optimization applies to both normal and upgrade modes, matching the
    # previous behavior where `update.sh` could be skipped with lazy updates.
    local should_sync="true"
    if [[ "${OT_LAZY_UPDATES}" == "true" ]] && ! is_update_metadata_changed; then
        print_debug "Skipping sync: metadata unchanged and lazy updates enabled."
        should_sync="false"
    fi

    if [[ "${should_sync}" == "true" ]]; then
        sync_environment
    fi

    # Write update-check metadata to disk if user has requested "lazy updates",
    # otherwise delete any old, leftover metadata to avoid clutter.
    if [[ "${OT_LAZY_UPDATES}" == "true" ]]; then
        print_debug "Saving current update-check metadata to disk..."
        save_update_metadata
    elif [[ -f "${OT_UPDATE_METADATA_FILE}" ]]; then
        print_debug "Deleting outdated update-check metadata from disk..."
        rm -f "${OT_UPDATE_METADATA_FILE}"
    fi
}
