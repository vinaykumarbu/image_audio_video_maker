@echo off
REM Image Audio Video Maker - Setup Script for Windows
REM This script builds the Docker image (run once)

echo ==========================================
echo Image Audio Video Maker - Setup
echo ==========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker is not installed!
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker is not running!
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

echo Docker is installed and running
echo.

REM Navigate to project directory
cd /d "%~dp0.."

echo Building Docker image...
echo This may take a few minutes on first run...
echo.

REM Build the Docker image
docker-compose build

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo Setup Complete!
    echo ==========================================
    echo.
    echo Next steps:
    echo 1. Add your image files to: input\images\
    echo 2. Add your audio files to: input\audio\
    echo 3. Run: windows\RUN_GENERATOR.bat
    echo.
) else (
    echo.
    echo ERROR: Docker build failed!
    echo Please check the error messages above.
    echo.
)

pause
