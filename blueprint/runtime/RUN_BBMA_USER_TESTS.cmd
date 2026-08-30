@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "SETTINGS=%SCRIPT_DIR%v459_user_test_settings.json"
if not exist "%SETTINGS%" (
  echo BLOCKED: Copy v459_user_test_settings.example.json to v459_user_test_settings.json and edit the four paths.
  exit /b 2
)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%v459_user_test_runner.ps1" -Mode RUN -Stage AUTO -SettingsPath "%SETTINGS%"
exit /b %ERRORLEVEL%
