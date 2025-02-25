from app import create_app
from app.extensions import db  # Import db from extensions
from flask_migrate import Migrate, upgrade

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Create tables (if they don't exist)
        db.create_all()

        # Apply any pending migrations
        upgrade()