import os
from flask import Flask
from dotenv import load_dotenv
from.extensions import init_extensions
from.config import config  # Import your 'config' dictionary

load_dotenv()  # For local development

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG') or 'default'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    init_extensions(app)

    from.main.routes import main
    from.auth.routes import auth
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    # Health check endpoint (for Render)
    @app.route('/ping')
    def ping():
        return 'pong'

    return app