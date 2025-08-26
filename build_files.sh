#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "=== Running build_files.sh ==="
# Install Python dependencies
python -m pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

echo "=== collectstatic finished ==="

ls -R staticfiles