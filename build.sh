#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Activate the virtual environment (if you're using one)
source.venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Database migrations
flask db init
flask db migrate
flask db upgrade