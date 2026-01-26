# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install FFMPEG and required system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Verify FFMPEG installation
RUN ffmpeg -version

# Copy the Python script
COPY generate_videos.py /app/

# Create input and output directories
RUN mkdir -p /app/input/images /app/input/audio /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the video generator script
CMD ["python", "generate_videos.py"]
