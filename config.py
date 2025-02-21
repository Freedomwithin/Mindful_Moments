import os
from dotenv import load_dotenv

load_dotenv()  # This line can be removed if you're not using a .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # Add any other configuration settings here