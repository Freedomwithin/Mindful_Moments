#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Install dependencies
pip install -r requirements.txt

# Database migrations
flask db migrate
flask db upgrade