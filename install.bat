@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

rem --- Generate ESC character for ANSI color codes ---
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "RED=%ESC%[31m" & set "YEL=%ESC%[33m" & set "GRN=%ESC%[92m" & set "CYAN=%ESC%[36m" & set "RESET=%ESC%[0m"

rem --- Constants ---
pushd "%~dp0" || call :die "Cannot cd to script directory"
set "SCRIPT_DIR=%CD%"

if not defined OT_PLATFORM_REQUIREMENTS (set "OT_PLATFORM_REQUIREMENTS=cuda")

rem --- Normalize legacy file-based values ---
if /i "%OT_PLATFORM_REQUIREMENTS%"=="requirements-cuda.txt" (set "OT_PLATFORM_REQUIREMENTS=cuda")
if /i "%OT_PLATFORM_REQUIREMENTS%"=="requirements-rocm.txt" (set "OT_PLATFORM_REQUIREMENTS=rocm")
if /i "%OT_PLATFORM_REQUIREMENTS%"=="requirements-default.txt" (set "OT_PLATFORM_REQUIREMENTS=cpu")

goto :main

rem --- Helpers ---
:die
  echo.
  echo %RED%ERROR:%RESET% %~1
  echo.
  pause
  popd
  (echo %CMDCMDLINE% | find /I "%~nx0" >nul) && exit /b 1 || exit 1

rem --- Main ---
:main

rem 1) Check for uv
echo %CYAN%Checking for uv package manager...%RESET%
where uv >nul 2>&1
if errorlevel 1 (
    echo %RED%uv is not installed or not in PATH.%RESET%
    echo.
    echo Install uv via one of:
    echo   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo   winget install --id=astral-sh.uv
    echo.
    echo See: https://docs.astral.sh/uv/getting-started/installation/
    call :die "uv is required to install OneTrainer."
)
echo %GRN%uv found.%RESET%

rem Force UTF-8 mode for Python
set "PYTHONUTF8=1"

rem 2) Sync environment
echo.
echo %CYAN%Installing dependencies (group: %OT_PLATFORM_REQUIREMENTS%)...%RESET%
echo Executing: uv sync --group %OT_PLATFORM_REQUIREMENTS%
uv sync --group %OT_PLATFORM_REQUIREMENTS% || call :die "uv sync failed"

rem 3) Check CUDA (if cuda group)
if /i "%OT_PLATFORM_REQUIREMENTS%"=="cuda" (
    echo.
    echo %CYAN%Checking CUDA availability...%RESET%
    uv run --group cuda python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 1)"
    if errorlevel 1 (
        echo %YEL%CUDA not found via torch.cuda.is_available.%RESET%
        set "ans_amd="
        set /p "ans_amd=AMD GPU? (y/n): "
        if /i "!ans_amd!"=="y" (
            echo Executing: uv run --group cuda python "%SCRIPT_DIR%\scripts\install_zluda.py"
            uv run --group cuda python "%SCRIPT_DIR%\scripts\install_zluda.py" || call :die "ZLUDA install failed"
        ) else (
            call :die "CUDA unavailable and not an AMD GPU setup - aborting. Please check PyTorch and NVIDIA driver compatibility."
        )
    ) else (
        echo %GRN%CUDA is available.%RESET%
    )
)

echo.
echo %GRN%**** Install successful^^! ****%RESET%
echo.
pause
popd
exit /b 0
