# OneTrainer Launch Scripts


## Prerequisites

OneTrainer uses [uv](https://docs.astral.sh/uv/) for dependency management. You must install uv before using any launch scripts.

**Linux / macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or via `winget install --id=astral-sh.uv`.

See the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) for more options.


## Mac and Linux Systems

### The launch system consists of the following scripts:

- `install.sh`: Detects your GPU platform and syncs all dependencies via uv.
- `update.sh`: Updates OneTrainer to the latest version and re-syncs dependencies.
- `start-ui.sh`: Launches the main OneTrainer interface.
- `run-cmd.sh`: Executes a custom script (such as "train"), and supports providing command-line arguments. See the "running custom script commands" guide section for more details.


### All of the scripts accept the following *optional* environment variables to customize their behavior:

- `OT_PLATFORM_REQUIREMENTS`: Allows you to override which GPU platform's dependencies to install. Defaults to `detect`, which automatically detects whether you have an AMD or NVIDIA GPU. Valid values are `cuda` for NVIDIA, `rocm` for AMD, and `cpu` for CPU-only systems. Legacy file-based values (`requirements-cuda.txt`, `requirements-rocm.txt`, `requirements-default.txt`) are also accepted for backward compatibility.

- `OT_LAZY_UPDATES`: If set to `true`, OneTrainer's self-update process will only re-sync dependencies if the OneTrainer source code has been modified since the previous sync. This speeds up executions of `update.sh`, and is generally safe, but may miss some updates and important bugfixes for external third-party dependencies. If you use this option, you must set it permanently for *every* script (not just `update.sh`). Defaults to `false`.

- `OT_CUDA_LOWMEM_MODE`: If set to `true`, it enables aggressive garbage collection in PyTorch to help with low-memory GPUs. Defaults to `false`.

- `OT_SCRIPT_DEBUG`: If set to `true`, it enables additional debug logging in the scripts. Defaults to `false`.


### Examples of how to use the custom environment variables:

- You can provide custom environment variables directly on the command line, as follows: `env OT_CUDA_LOWMEM_MODE="true" OT_PLATFORM_REQUIREMENTS="cuda" ./start-ui.sh`.
- You can add them to your user's persistent environment variables, so that they are always active. The process varies depending on your operating system. On Linux, you can place them in `~/.config/environment.d/onetrainer.conf` (on all Systemd-based distros), which is a plaintext file with *one variable per line,* such as `OT_CUDA_LOWMEM_MODE="true"`. Beware that changes to `environment.d` requires a *complete system restart* to take effect (there is no command for reloading them live). To verify that your environment has been set persistently, you can then open a terminal window and run `printenv <variable name>` (such as `printenv OT_CUDA_LOWMEM_MODE`) to see if your custom values have taken effect.
- If you're launching OneTrainer from your own, custom scripts, then you can instead `export` the new values (which tells the shell to pass those environment variables onto child processes). For example, by having a line such as `export OT_CUDA_LOWMEM_MODE="true"` before your script calls `./OneTrainer/start-ui.sh`.
- If you're running OneTrainer inside a Docker/Podman container, you can instead use the [ENV](https://docs.docker.com/reference/dockerfile/#env) instruction in your `Dockerfile` / `Containerfile` to set the variables, such as `ENV OT_CUDA_LOWMEM_MODE="true"`.


### Installing a specific Python version:

uv automatically manages Python installations. The required Python version (3.10) is pinned in the `.python-version` file at the root of the project. If you need a different version, you can override it with `uv python pin <version>`.


### Running custom script commands:

- Always use `run-cmd.sh` when you want to execute any of OneTrainer's CLI tasks. It automatically validates the chosen target script's name, configures the runtime environment correctly, and then runs the target script with your given command-line arguments.
- For example, to run the training CLI script, you would use `./run-cmd.sh train --config-path <path to your config>`.
- The names of all valid scripts can be seen in OneTrainer's `scripts/` sub-directory.
- To learn more about the available command-line arguments for each script, you can execute them with the `-h` (help) argument: `./run-cmd.sh <script name> -h`. For example, if you want to learn more about the "train" script, you would run `./run-cmd.sh train -h`.


### Creating your own launch scripts and automating tasks:

- If you want to automate various OneTrainer CLI tasks, then you should call `run-cmd.sh` from your own scripts (see previous guide section), since it's capable of running *any* OneTrainer command with your own command-line arguments.
- To run multiple tasks in the same scripts, you should perform separate calls to `run-cmd.sh`. Run it as many times as required for all the custom scripts and command-line arguments that you want to perform in your own script.
- It's highly recommended that you use `set -e` at the top of your own scripts (see `install.sh` for an example of that), since it tells Bash to exit your script if any of the OneTrainer commands fail. Otherwise your script will continue running even if a previous step has failed, which is usually not what you want!


## Windows Systems

### The launch system consists of the following scripts:

- `install.bat`: Checks for uv, syncs dependencies, and verifies CUDA availability.
- `update.bat`: Updates OneTrainer to the latest version and re-syncs dependencies.
- `start-ui.bat`: Launches the main OneTrainer interface.
- `export_debug.bat`: Generates a debug report for troubleshooting.


### Environment variables for Windows:

- `OT_PLATFORM_REQUIREMENTS`: Sets which GPU platform to use. Defaults to `cuda`. Valid values are `cuda`, `rocm`, and `cpu`.

Set environment variables before running the batch file, for example:
```
set OT_PLATFORM_REQUIREMENTS=cpu
start-ui.bat
```
