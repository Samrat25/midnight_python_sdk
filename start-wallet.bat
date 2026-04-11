@echo off
echo ========================================
echo   Starting Midnight Wallet
echo ========================================
echo.

echo [1/2] Starting Backend API...
start "Midnight API" cmd /k "python wallet-app\api\server.py"
timeout /t 3 /nobreak >nul

echo [2/2] Opening Wallet in Browser...
start "" "%CD%\wallet-app\index.html"

echo.
echo ========================================
echo   Wallet Started!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Wallet UI: Opening in browser...
echo.
echo Press any key to stop the API server...
pause >nul

taskkill /FI "WINDOWTITLE eq Midnight API*" /T /F >nul 2>&1
