#!/bin/bash

# Apply database migrations
python manage.py migrate

# Create static directories if they don't exist
mkdir -p frontend/static
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --noinput --clear

# Execute the command passed to docker
exec "$@"