#!/bin/bash

# Image Audio Video Maker - Setup Script for Mac
# This script builds the Docker image (run once)

echo "=========================================="
echo "Image Audio Video Maker - Setup"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ ERROR: Docker is not installed!"
    echo ""
    echo "Please install Docker Desktop from:"
    echo "https://www.docker.com/products/docker-desktop"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ ERROR: Docker is not running!"
    echo ""
    echo "Please start Docker Desktop and try again."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Navigate to project directory
cd "$PROJECT_DIR" || exit 1

echo "Building Docker image..."
echo "This may take a few minutes on first run..."
echo ""

# Build the Docker image
docker-compose build

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Add your image files to: input/images/"
    echo "2. Add your audio files to: input/audio/"
    echo "3. Run: mac/RUN_GENERATOR.sh"
    echo ""
else
    echo ""
    echo "❌ ERROR: Docker build failed!"
    echo "Please check the error messages above."
    echo ""
fi

read -p "Press Enter to exit..."
