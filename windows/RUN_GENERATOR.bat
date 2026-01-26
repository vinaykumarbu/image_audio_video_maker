@echo off
REM Image Audio Video Maker - Run Script for Windows
REM This script processes images and audio files to generate videos

echo ==========================================
echo Image Audio Video Maker
echo ==========================================
echo.

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

REM Navigate to project directory
cd /d "%~dp0.."

REM Check if Docker image exists
docker images | findstr "image_audio_video_maker" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker image not found!
    echo.
    echo Please run the setup script first:
    echo   windows\SETUP.bat
    echo.
    pause
    exit /b 1
)

REM Count input files
set IMAGE_COUNT=0
set AUDIO_COUNT=0

for %%f in (input\images\*.jpg input\images\*.jpeg input\images\*.png input\images\*.bmp) do set /a IMAGE_COUNT+=1
for %%f in (input\audio\*.mp3 input\audio\*.wav input\audio\*.m4a input\audio\*.aac input\audio\*.flac) do set /a AUDIO_COUNT+=1

echo Image files found: %IMAGE_COUNT%
echo Audio files found: %AUDIO_COUNT%
echo.

if %IMAGE_COUNT% EQU 0 (
    echo WARNING: No image files found!
    echo.
    echo Please add files to:
    echo   - input\images\ (for image files^)
    echo   - input\audio\ (for audio files^)
    echo.
    echo Remember: Image and audio filenames must match!
    echo Example: 1_shloka.jpg + 1_shloka.mp3
    echo.
    pause
    exit /b 0
)

if %AUDIO_COUNT% EQU 0 (
    echo WARNING: No audio files found!
    echo.
    echo Please add files to:
    echo   - input\images\ (for image files^)
    echo   - input\audio\ (for audio files^)
    echo.
    echo Remember: Image and audio filenames must match!
    echo Example: 1_shloka.jpg + 1_shloka.mp3
    echo.
    pause
    exit /b 0
)

echo Starting video generation...
echo.

REM Run the Docker container
docker-compose up

echo.
echo ==========================================
echo Process Complete!
echo ==========================================
echo.
echo Check the output\ folder for your videos.
echo.
pause
