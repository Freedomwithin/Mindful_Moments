#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Upgrade pip and install requirements
echo "Upgrading pip and installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Set Flask application
export FLASK_APP=flask_app.py
echo "FLASK_APP set to $FLASK_APP"

# Debug: Print environment variables
echo "DEBUG: Environment variables:"
env | grep -E "DATABASE_URL|SQLALCHEMY_DATABASE_URI|SECRET_KEY|FLASK_DEBUG"

# Initialize and apply database migrations
echo "Initializing and applying database migrations..."
flask db init || true  # Initialize if not already initialized
flask db migrate -m "Migration from build script" || true
flask db upgrade || true

# Debug: Print migration history
echo "DEBUG: Migration history:"
flask db history || echo "No migration history available"

# Manually create database tables if needed
echo "Creating database tables..."
python << END
from flask_app import app, db
with app.app_context():
    db.create_all()
END

echo "Build process completed."