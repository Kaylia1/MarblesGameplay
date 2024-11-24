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
echo %DEFAULT_BRANCH%

:: Construct the download URL for the default branch
set REPO_URL=https://github.com/%USERNAME%/%REPO%/archive/refs/heads/%DEFAULT_BRANCH%.zip

:: Set the temporary download and extraction folder
set DOWNLOAD_DIR=%TEMP%\github_repo_download

:: Create the download directory if it doesn't exist
if not exist "%DOWNLOAD_DIR%" mkdir "%DOWNLOAD_DIR%"

:: Download the repository as a .zip file
echo Downloading repository from %REPO_URL%...
curl -L %REPO_URL% -o "%DOWNLOAD_DIR%\repo.zip" || (
    echo Failed to download repository. Exiting...
    pause
    exit /b
)

:: Unzip the repository into the temporary folder
echo Unzipping repository...
powershell -Command "Expand-Archive -Path '%DOWNLOAD_DIR%\repo.zip' -DestinationPath '%DOWNLOAD_DIR%' -Force" || (
    echo Failed to unzip repository. Exiting...
    pause
    exit /b
)

:: Find the unzipped folder (assumes standard naming: repository-branch)
:: Detect the extracted directory
for /d %%I in ("%DOWNLOAD_DIR%\*") do (
    set "EXTRACTED_DIR=%%I"
)
if not defined EXTRACTED_DIR (
    echo Extracted directory not found. Exiting...
    pause
    exit /b
)

:: Replace files in the root directory with the unzipped files
echo Replacing files in "%SCRIPT_DIR%"...
xcopy /E /Y /I "%EXTRACTED_DIR%\*" "%SCRIPT_DIR%"

:: Clean up temporary files
echo Cleaning up temporary files...
rd /s /q "%DOWNLOAD_DIR%"

echo Update completed successfully!
pause