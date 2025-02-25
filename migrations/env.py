import logging
from logging.config import fileConfig
import os
from sqlalchemy import create_engine

from app import app  # Import your Flask app instance
from app.models import db  # Import your db instance

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the.ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

def get_engine():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    print(f"DATABASE_URL: {DATABASE_URL}")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set.")
    return create_engine(DATABASE_URL)

def get_engine_url():
    return os.environ.get("DATABASE_URL").replace('%', '%%')  # Simplified

#... (remove target_db and offline migration code)...

def get_metadata():
    return db.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
        )

        with context.begin_transaction():
            print("Before running migrations (online)...")
            context.run_migrations()
            print("After running migrations (online)...")

run_migrations_online()