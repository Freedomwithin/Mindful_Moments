#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Install dependencies
pip install -r requirements.txt

#Attemp to rm migatations on render
rm -rf migrations 
rm instance/your_database.db

# Database migrations
flask db init 
flask db migrate
flask db upgrade