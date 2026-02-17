@echo off
setlocal EnableDelayedExpansion

REM Avoid footgun by explictly navigating to the directory containing the batch file
cd /d "%~dp0"

REM Verify that OneTrainer is our current working directory
if not exist "scripts\train_ui.py" (
    echo Error: train_ui.py does not exist, you have done something very wrong. Reclone the repository.
    goto :end_error
)

if not defined OT_PLATFORM_REQUIREMENTS (set "OT_PLATFORM_REQUIREMENTS=cuda")

rem --- Normalize legacy file-based values ---
if /i "%OT_PLATFORM_REQUIREMENTS%"=="requirements-cuda.txt" (set "OT_PLATFORM_REQUIREMENTS=cuda")
if /i "%OT_PLATFORM_REQUIREMENTS%"=="requirements-rocm.txt" (set "OT_PLATFORM_REQUIREMENTS=rocm")
if /i "%OT_PLATFORM_REQUIREMENTS%"=="requirements-default.txt" (set "OT_PLATFORM_REQUIREMENTS=cpu")

REM Check for uv
where uv >nul 2>&1
if errorlevel 1 (
    echo Error: uv is not installed. Please run install.bat first or install uv manually.
    goto :end_error
)

REM Force UTF-8 mode for Python (prevents encoding errors with non-ASCII paths/data)
set "PYTHONUTF8=1"

REM Disable HF_HUB_DISABLE_XET, buggy; default disables Xet (set to 0 to enable) - https://github.com/Nerogar/OneTrainer/issues/949
if not defined HF_HUB_DISABLE_XET (
    set "HF_HUB_DISABLE_XET=1"
)
echo HF_HUB_DISABLE_XET=%HF_HUB_DISABLE_XET%
echo.
echo NOTE: Xet disabled, to enable it set as 0 before launch

:launch
echo Starting UI...
if defined PROFILE (
    uv run --group %OT_PLATFORM_REQUIREMENTS% python -m scalene --off --cpu --gpu --profile-all --no-browser scripts\train_ui.py
) else (
    uv run --group %OT_PLATFORM_REQUIREMENTS% python scripts\train_ui.py
)
if errorlevel 1 (
    echo Error: UI script exited with code %ERRORLEVEL%
    pause
    exit /b 1
)

:end
pause
exit /b 0

:end_error
pause
exit /b 1
