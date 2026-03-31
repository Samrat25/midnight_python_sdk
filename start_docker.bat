@echo off
REM Start Midnight services using Docker (Windows)

echo.
echo ========================================
echo   Starting Midnight Services with Docker
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running. Please start Docker Desktop first.
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Choose which docker-compose to use
if "%1"=="--real" (
    echo Using real Midnight Docker images...
    set COMPOSE_FILE=docker-compose.real.yml
) else (
    echo Using local mock services...
    set COMPOSE_FILE=docker-compose.local.yml
)

echo Compose file: %COMPOSE_FILE%
echo.

REM Stop any existing containers
echo Stopping existing containers...
docker-compose -f %COMPOSE_FILE% down 2>nul

REM Build and start services
echo.
echo Building and starting services...
docker-compose -f %COMPOSE_FILE% up -d --build

REM Wait for services to be healthy
echo.
echo Waiting for services to be healthy...
timeout /t 5 /nobreak >nul

REM Check service status
echo.
echo Checking service status...
docker-compose -f %COMPOSE_FILE% ps

echo.
echo ========================================
echo [OK] Services started!
echo.
echo Check status with:
echo   midnight-py status
echo.
echo View logs with:
echo   docker-compose -f %COMPOSE_FILE% logs -f
echo.
echo Stop services with:
echo   docker-compose -f %COMPOSE_FILE% down
echo ========================================
echo.
