import os
from flask import Flask
from dotenv import load_dotenv
from.extensions import init_extensions
from.config import config  # Import your 'config' dictionary

load_dotenv()  # For local development; Render will use environment variables

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG') or 'default'  # Get config name from environment or use default
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # Load config from your 'config' dictionary

    # No need to set app.debug here; it's controlled by the configuration

    # Consider enabling CSRF protection for production:
    # if app.config['ENV'] == 'production':
    #     app.config['WTF_CSRF_ENABLED'] = True

    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        # You might want to use a logging mechanism here for production
        raise ValueError("No SECRET_KEY set. Set it in Render environment variables")
    app.config['SECRET_KEY'] = SECRET_KEY

    init_extensions(app)

    from.main.routes import main
    from.auth.routes import auth
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app