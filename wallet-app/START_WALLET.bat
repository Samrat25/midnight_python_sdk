@echo off
echo ========================================
echo   Midnight Wallet - Quick Start
echo ========================================
echo.

REM Check if backend is already running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Backend API is already running
) else (
    echo [STARTING] Backend API...
    start "Midnight Wallet API" python api/server.py
    timeout /t 3 /nobreak >nul
    echo [OK] Backend API started on http://localhost:8000
)

echo.
echo [OPENING] Wallet in browser...
echo.

REM Open wallet in default browser
start "" "%CD%\index.html"

echo ========================================
echo   Wallet opened successfully!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Wallet UI: file:///%CD%\index.html
echo.
echo Press any key to exit...
pause >nul
