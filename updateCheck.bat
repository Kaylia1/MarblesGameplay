@echo off
:: Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

:: Set the GitHub repository and API URL
set USERNAME=Kaylia1
set REPO=MarblesGameplay
set API_URL=https://api.github.com/repos/%USERNAME%/%REPO%

:: Fetch the default branch using curl
for /f "tokens=*" %%A in ('curl -s %API_URL% ^| findstr /i "default_branch"') do (
    for /f "tokens=2 delims=:, " %%B in ("%%A") do set DEFAULT_BRANCH=%%B
)

:: Remove double quotes from DEFAULT_BRANCH if present
set DEFAULT_BRANCH=%DEFAULT_BRANCH:"=%

:: Verify that DEFAULT_BRANCH was set
if "%DEFAULT_BRANCH%"=="" (
    echo Failed to fetch the default branch. Exiting...
    pause
    exit /b
)

:: Fetch the latest commit hash from GitHub
for /f "tokens=*" %%A in ('curl -s %API_URL%/commits/%DEFAULT_BRANCH% ^| findstr /i "sha" ^| findstr /i /v "parent"') do (
    for /f "tokens=2 delims=:, " %%B in ("%%A") do set REMOTE_COMMIT=%%B
)

:: Remove double quotes from REMOTE_COMMIT if present
set REMOTE_COMMIT=%REMOTE_COMMIT:"=%

:: Define the path for the stored commit hash file
set LOCAL_HASH_FILE=%SCRIPT_DIR%local_commit_hash.txt

:: Check if the local hash file exists
if exist "%LOCAL_HASH_FILE%" (
    :: Read the local commit hash from the file
    for /f "tokens=*" %%A in (%LOCAL_HASH_FILE%) do set LOCAL_COMMIT=%%A
) else (
    :: Initialize the local commit hash as empty if the file doesn't exist
    set LOCAL_COMMIT=
)

:: Remove trailing spaces from LOCAL_COMMIT
set LOCAL_COMMIT=%LOCAL_COMMIT: =%

:: Compare the local and remote commit hashes
if "%REMOTE_COMMIT%"=="%LOCAL_COMMIT%" (
    echo Your local repository is up to date.
) else (
    echo An update is available. Latest commit hash: %REMOTE_COMMIT%
    echo Your local commit hash: %LOCAL_COMMIT%
    echo Saving the new commit hash locally...
    echo %REMOTE_COMMIT% > "%LOCAL_HASH_FILE%"
    call updateCode.bat
)