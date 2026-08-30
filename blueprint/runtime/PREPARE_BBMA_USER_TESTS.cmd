@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "SETTINGS=%SCRIPT_DIR%v459_user_test_settings.json"
if not exist "%SETTINGS%" (
  copy "%SCRIPT_DIR%v459_user_test_settings.example.json" "%SETTINGS%" >nul
  echo Created: %SETTINGS%
  echo Edit the four paths, then run this file again.
  exit /b 2
)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%v459_user_test_runner.ps1" -Mode PREPARE -SettingsPath "%SETTINGS%"
exit /b %ERRORLEVEL%
