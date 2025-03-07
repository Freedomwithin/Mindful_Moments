import os
from flask import Flask
from .extensions import db, login_manager, init_extensions  # Import db and login_manager
from .config import config

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG') or 'default'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    if app.config['ENV'] == 'production':
        app.config['WTF_CSRF_ENABLED'] = True

    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        raise ValueError("No SECRET_KEY set. Set it in Render environment variables.")
    app.config['SECRET_KEY'] = secret_key

    # ***CRITICAL CHANGE: PostgreSQL Configuration (Use DATABASE_URL)***
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    if not app.config['SQLALCHEMY_DATABASE_URI']:  # Important check
        raise ValueError("No DATABASE_URL set. Set it in Render environment variables.")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Good practice

    init_extensions(app)  # Initialize extensions *after* setting the URI

    from .models import User  # Import the User model here
    from .main.routes import main
    from .auth.routes import auth
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    @app.route('/ping')
    def ping():
        return 'pong'

    # Initialize flask_login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login page if not logged in

    @login_manager.user_loader
    def load_user(user_id):
        # Load the user from the database based on user_id
        return User.query.get(int(user_id))

    return app