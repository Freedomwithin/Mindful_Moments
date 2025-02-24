import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from.env locally

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # No default here for production!
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASE_DIR, '..', 'instance', 'your_database.db')  # Default local DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'  # Get debug mode from environment
    WTF_CSRF_ENABLED = True
    LOGIN_DISABLED = False

    @classmethod
    def init_app(cls, app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YourDevSecretKey'  # Default for development

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory DB for testing
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YourTestSecretKey'

class ProductionConfig(Config):
    DEBUG = False
    # No default SECRET_KEY here! It MUST be set in.env or environment variables

config = {  # Keep 'config' as you have it
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}