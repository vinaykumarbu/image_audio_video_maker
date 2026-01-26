#!/bin/bash

# Image Audio Video Maker - Run Script for Mac
# This script processes images and audio files to generate videos

echo "=========================================="
echo "Image Audio Video Maker"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ ERROR: Docker is not running!"
    echo ""
    echo "Please start Docker Desktop and try again."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Navigate to project directory
cd "$PROJECT_DIR" || exit 1

# Check if Docker image exists
if ! docker images | grep -q "image_audio_video_maker"; then
    echo "❌ ERROR: Docker image not found!"
    echo ""
    echo "Please run the setup script first:"
    echo "  mac/SETUP.sh"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Count input files
IMAGE_COUNT=$(find input/images -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.bmp" \) 2>/dev/null | wc -l | tr -d ' ')
AUDIO_COUNT=$(find input/audio -type f \( -iname "*.mp3" -o -iname "*.wav" -o -iname "*.m4a" -o -iname "*.aac" -o -iname "*.flac" \) 2>/dev/null | wc -l | tr -d ' ')

echo "📸 Image files found: $IMAGE_COUNT"
echo "🎵 Audio files found: $AUDIO_COUNT"
echo ""

if [ "$IMAGE_COUNT" -eq 0 ] || [ "$AUDIO_COUNT" -eq 0 ]; then
    echo "⚠️  WARNING: No input files found!"
    echo ""
    echo "Please add files to:"
    echo "  - input/images/ (for image files)"
    echo "  - input/audio/ (for audio files)"
    echo ""
    echo "Remember: Image and audio filenames must match!"
    echo "Example: 1_shloka.jpg + 1_shloka.mp3"
    echo ""
    read -p "Press Enter to exit..."
    exit 0
fi

echo "🚀 Starting video generation..."
echo ""

# Run the Docker container
docker-compose up

echo ""
echo "=========================================="
echo "✅ Process Complete!"
echo "=========================================="
echo ""
echo "Check the output/ folder for your videos."
echo ""
read -p "Press Enter to exit..."
