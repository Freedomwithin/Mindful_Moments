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
if [ -f "models.py" ]; then
    echo "models.py found"
else
    echo "ERROR: models.py not found"
    exit 1
fi

# Upgrade pip and install requirements
echo "Upgrading pip and installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Print Python version and installed packages
echo "DEBUG: Python version:"
python --version
echo "DEBUG: Installed packages:"
pip list

# Initialize and apply database migrations
echo "Initializing and applying database migrations..."
flask db init || true  # Initialize if not already initialized
flask db migrate -m "Migration from build script"
flask db upgrade

echo "Build process completed."

# Note: We're not deactivating the virtual environment here