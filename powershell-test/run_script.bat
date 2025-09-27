@echo off
REM --- This batch file executes the PowerShell script ---

REM Define the name of the PowerShell script
set PS_SCRIPT="download_data.ps1"

REM Check if the PowerShell script exists in the current directory
if not exist %PS_SCRIPT% (
    echo Error: The file %PS_SCRIPT% was not found in the current directory.
    pause
    exit /b 1
)

REM Executes the PowerShell script.
REM -NoProfile: Does not load the current user's profile, making it run faster.
REM -ExecutionPolicy Bypass: Allows the script to run without modifying the system's security settings.
REM -File: Specifies the script to run.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File %PS_SCRIPT%

pause