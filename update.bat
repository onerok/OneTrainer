@echo off
setlocal EnableDelayedExpansion

rem --- Generate ESC character for ANSI color codes ---
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "RED=%ESC%[31m" & set "YEL=%ESC%[33m" & set "GRN=%ESC%[92m" & set "CYAN=%ESC%[36m" & set "RESET=%ESC%[0m"

REM Avoid footgun by explictly navigating to the directory containing the batch file
cd /d "%~dp0"

REM Verify that OneTrainer is our current working directory
if not exist "scripts\train_ui.py" (
    echo %RED%Error: train_ui.py does not exist, you have done something very wrong. Reclone the repository.%RESET%
    goto :end_error
)

if not defined OT_PLATFORM_REQUIREMENTS (set "OT_PLATFORM_REQUIREMENTS=cuda")
if not defined GIT (set "GIT=git")

rem --- Normalize legacy file-based values ---
if /i "%OT_PLATFORM_REQUIREMENTS%"=="requirements-cuda.txt" (set "OT_PLATFORM_REQUIREMENTS=cuda")
if /i "%OT_PLATFORM_REQUIREMENTS%"=="requirements-rocm.txt" (set "OT_PLATFORM_REQUIREMENTS=rocm")
if /i "%OT_PLATFORM_REQUIREMENTS%"=="requirements-default.txt" (set "OT_PLATFORM_REQUIREMENTS=cpu")

rem --- Check for uv ---
where uv >nul 2>&1
if errorlevel 1 (
    echo %RED%uv is not installed. Please run install.bat first or install uv manually.%RESET%
    goto :end_error
)

:git_pull
echo %CYAN%Checking repository and branch information...%RESET%

REM Get current branch name
FOR /F "tokens=* USEBACKQ" %%F IN (`"%GIT%" rev-parse --abbrev-ref HEAD`) DO (
    set "current_branch=%%F"
)
echo Current branch: %current_branch%

REM Determine tracking information (remote and branch)
set "tracking_info="
FOR /F "tokens=* USEBACKQ" %%F IN (`"%GIT%" rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2^>NUL`) DO (
    set "tracking_info=%%F"
)

if not defined tracking_info (
    echo INFO: Current branch has no tracking remote configured.
    echo      This is normal for local-only branches.
    echo      Updates cannot be pulled automatically. Configure tracking with:
    echo      git branch --set-upstream-to=origin/master %current_branch%
) else (
    for /F "tokens=1,2 delims=/" %%a in ("!tracking_info!") do (
        set "tracking_remote=%%a"
        set "tracking_branch=%%b"
    )
    echo Tracking: !tracking_info!

    FOR /F "tokens=* USEBACKQ" %%F IN (`"!GIT!" config --get remote.!tracking_remote!.url 2^>NUL`) DO (
        set "remote_url=%%F"
    )
    echo Remote !tracking_remote!: !remote_url!

    set "is_official_repo="
    echo !remote_url! | findstr /i "Nerogar/OneTrainer" >nul && set "is_official_repo=1"

    set "is_master_branch="
    if /I "!tracking_branch!"=="master" (set "is_master_branch=1")

    if not defined is_official_repo (set "non_standard_setup=1")
    if not defined is_master_branch (set "non_standard_setup=1")

    if defined non_standard_setup (
        echo INFO: Non-standard repository setup detected:
        if not defined is_official_repo echo        - Using non-official repository: !remote_url!
        if not defined is_master_branch echo        - On branch !tracking_branch! instead of master
        echo      This is normal if you're using a fork or working on a specific branch.
    )

    REM Get current commit hash
    FOR /F "tokens=* USEBACKQ" %%F IN (`"%GIT%" rev-parse HEAD`) DO (
        set "local_commit=%%F"
    )
    echo Local commit: !local_commit:~0,8!...

    echo Fetching updates...
    "%GIT%" fetch !tracking_remote!
    if errorlevel 1 (
        echo %RED%Error: Could not fetch updates%RESET%
        goto :end_error
    )

    REM Get remote commit hash
    FOR /F "tokens=* USEBACKQ" %%F IN (`"%GIT%" rev-parse !tracking_remote!/!tracking_branch!`) DO (
        set "remote_commit=%%F"
    )
    echo Remote commit: !remote_commit:~0,8!...

    if "!local_commit!"=="!remote_commit!" (
        echo Repository is already up to date, skipping pull.
    ) else (
        echo Updates available, pulling changes...
        "%GIT%" pull
        if errorlevel 1 (
            echo %RED%Error: Git pull failed.%RESET%
            goto :end_error
        )
    )
)

rem --- Sync environment ---
echo.
echo %CYAN%Syncing dependencies (group: %OT_PLATFORM_REQUIREMENTS%)...%RESET%
echo Executing: uv sync --group %OT_PLATFORM_REQUIREMENTS%
uv sync --group %OT_PLATFORM_REQUIREMENTS%
if errorlevel 1 (
    echo %RED%Error: uv sync failed.%RESET%
    goto :end_error
)

:end_success
echo.
echo %GRN%***********%RESET%
echo %GRN%Update done%RESET%
echo %GRN%***********%RESET%
pause
exit /b 0

:end_error
echo.
echo %RED%*******************%RESET%
echo %RED%Error during update%RESET%
echo %RED%*******************%RESET%
pause
exit /b 1
