@echo off

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

REM Force UTF-8 mode for Python
set "PYTHONUTF8=1"

:launch
echo Generating debug report...
uv run --group %OT_PLATFORM_REQUIREMENTS% python scripts\generate_debug_report.py
if errorlevel 1 (
    echo Error: Debug report generation failed with code %ERRORLEVEL%
    pause
    exit /b 1
) else (
    echo Now upload the debug report to your Github issue or post in Discord.
)

:end
pause
exit /b 0

:end_error
pause
exit /b 1
