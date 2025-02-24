import os
from flask import Flask
from .extensions import init_extensions  # Correct relative import
from .config import config  # Correct relative import
from flask_migrate import Migrate

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

    # Database Configuration (Corrected - using app.root_path):
    db_path = os.path.join(app.root_path, 'your_database.db')  # Or my_database.db if renamed
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path  # 3 slashes are essential

    init_extensions(app)  # Initialize extensions *after* setting the URI

    from .models import db  # Correct relative import
    migrate = Migrate(app, db)  # Initialize Migrate *after* db is initialized with app

    from .main.routes import main  # Correct relative import
    from .auth.routes import auth  # Correct relative import
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    @app.route('/ping')
    def ping():
        return 'pong'

    return app