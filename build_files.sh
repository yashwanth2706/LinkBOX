#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput