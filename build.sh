#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Install dependencies
pip install -r requirements.txt

# Update Alembic version
psql $DATABASE_URL -f update_alembic_version.sql

# Database migrations
flask db init
flask db migrate
flask db upgrade