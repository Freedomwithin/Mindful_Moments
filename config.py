import os
from dotenv import load_dotenv

load_dotenv()  # This line can be removed if you're not using a .env file

class Config:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    print(f"DEBUG: DATABASE_URL from environment: {DATABASE_URL}")

    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        print(f"DEBUG: Modified DATABASE_URL: {DATABASE_URL}")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///instance/journal.db'
    print(f"DEBUG: Final SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # Add any other configuration settings here