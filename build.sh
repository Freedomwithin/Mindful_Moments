#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Set Flask application
export FLASK_APP=flask_app.py
echo "FLASK_APP set to $FLASK_APP"

# Upgrade pip and install requirements
echo "Upgrading pip and installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build process completed."

# Deactivate virtual environment
deactivate