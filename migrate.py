from app import create_app
from app.extensions import db  # Import db from extensions
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Add any migration commands you need here, e.g.:
        from flask_migrate import upgrade
        upgrade()