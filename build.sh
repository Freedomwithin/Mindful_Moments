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

# Verify DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "Warning: DATABASE_URL is not set. Please ensure it's set in your Render dashboard."
else
    echo "DATABASE_URL is set"
fi

# Check if SECRET_KEY is set, if not, generate a random one
if [ -z "$SECRET_KEY" ]; then
    echo "SECRET_KEY is not set. Generating a random one."
    export SECRET_KEY=$(python -c 'import os; print(os.urandom(16).hex())')
fi
echo "SECRET_KEY is set"

# Upgrade pip and install requirements
echo "Upgrading pip and installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize and apply database migrations
echo "Initializing and applying database migrations..."
flask db init || true  # Initialize if not already initialized
flask db migrate -m "Migration from build script"
flask db upgrade

echo "Build process completed."

# Note: We're not deactivating the virtual environment here