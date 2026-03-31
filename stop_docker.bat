@echo off
REM Stop Midnight Docker services (Windows)

echo.
echo ============================
echo   Stopping Midnight Services
echo ============================
echo.

REM Stop local services
if exist docker-compose.local.yml (
    echo Stopping local services...
    docker-compose -f docker-compose.local.yml down
)

REM Stop real services
if exist docker-compose.real.yml (
    echo Stopping real services...
    docker-compose -f docker-compose.real.yml down
)

echo.
echo [OK] All services stopped
echo.
