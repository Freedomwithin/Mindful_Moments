import logging
from logging.config import fileConfig

import os

from flask import current_app

from alembic import context
from sqlalchemy import create_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# CRITICAL CHANGE: Use DATABASE_URL from environment
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URI:
    raise ValueError("DATABASE_URL environment variable is not set.")

def get_metadata():
    try:
        return current_app.extensions['migrate'].db.metadata
    except AttributeError:  # For handling cases where current_app might not be available
        from app.models import db  # Import db directly
        return db.metadata

def get_engine_url(config):  # Add config as a parameter
    try:
        return get_engine(config).url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except AttributeError:
        return str(get_engine(config).url).replace('%', '%%')

def get_engine(config):  # Add config as a parameter
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine

config.set_main_option('sqlalchemy.url', get_engine_url(config))  # Pass config here

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = SQLALCHEMY_DATABASE_URI  # Use the environment variable
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args if current_app else {}  # Handle potential absence of current_app
    if conf_args and conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = create_engine(SQLALCHEMY_DATABASE_URI)  # Use create_engine with the env variable

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()