import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))  # Define basedir here

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uqRtbM8W3lzk3zuYJbLyyBf1zaHxkOU9u6Rupd3zsMk' 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'production'  # Set the environment to 'production'

    @classmethod
    def init_app(cls, app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for testing
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Config,  # Use the base Config for production
    'default': DevelopmentConfig
}