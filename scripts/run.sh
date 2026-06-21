#!/bin/bash

echo "Launching ATS_16.1..."

# Go to project root (parent of scripts)
cd "$(dirname "$0")/.."

# Run the app from bin
python3 bin/app.py
