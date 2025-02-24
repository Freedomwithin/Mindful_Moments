import os
from flask import Flask
from dotenv import load_dotenv
from.extensions import init_extensions
from.config import config

# Load environment variables from.env locally (not needed on Render)
load_dotenv()  

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG') or 'default'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Enable CSRF protection in production
    if app.config['ENV'] == 'production':
        app.config['WTF_CSRF_ENABLED'] = True 

    # Get the secret key from environment variables
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        raise ValueError("No SECRET_KEY set. Set it in Render environment variables.")
    app.config['SECRET_KEY'] = secret_key

    # Initialize Flask extensions
    init_extensions(app)

    # Register blueprints
    from.main.routes import main
    from.auth.routes import auth
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    # Health check endpoint (for Render)
    @app.route('/ping')
    def ping():
        return 'pong'

    return app