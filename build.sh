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

# Debug: Print environment variables
echo "DEBUG: Environment variables:"
env | grep -E "DATABASE_URL|SQLALCHEMY_DATABASE_URI|SECRET_KEY|FLASK_DEBUG"

# Check if models.py exists
echo "DEBUG: Checking for models.py"
if [ -f "models.