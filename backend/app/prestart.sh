#! /usr/bin/env bash

# Let the DB start
pypy3 /app/app/backend_pre_start.py

# Run migrations
# alembic upgrade head

# Create initial data in DB
pypy3 /app/app/initial_data.py
