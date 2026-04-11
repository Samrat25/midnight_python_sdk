@echo off
REM Midnight Wallet - Quick Open Script
REM Opens the wallet in your default browser without needing to navigate

echo ========================================
echo   Opening Midnight Wallet...
echo ========================================
echo.

REM Check if backend is running
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Midnight Wallet API*" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Backend API is running
) else (
    echo [STARTING] Backend API...
    start "Midnight Wallet API" python api/server.py
    timeout /t 2 /nobreak >nul
    echo [OK] Backend started
)

echo.
echo [OPENING] Wallet in browser...
echo.

REM Open the new V2 wallet
start "" "%CD%\index-v2.html"

echo ========================================
echo   Wallet opened!
echo ========================================
echo.
echo Wallet: file:///%CD%\index-v2.html
echo Backend: http://localhost:8000
echo.
echo Features:
echo  - Modern Lace-inspired UI
echo  - Unshielded transfers (public)
echo  - Shielded transfers (private)
echo  - DUST generation
echo  - Transaction history
echo  - Airdrop function
echo.
echo Press any key to exit...
pause >nul
