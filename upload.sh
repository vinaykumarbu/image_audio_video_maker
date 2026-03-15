#!/bin/bash
# Helper script to upload videos to Google Drive

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Run the upload script with all arguments passed to this script
python3 upload_to_gdrive.py "$@"
