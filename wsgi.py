import os
from app import create_app  # Import create_app from app/__init__.py

config_name = os.getenv('FLASK_CONFIG') or 'production'  # Get config name from environment
app = create_app(config_name)  # Create the Flask app instance

# No app.run() here! Render handles the running of the app.