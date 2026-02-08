#!/bin/bash

# Let the DB start (optional sleep or pg_isready equivalent)
echo "Waiting for SQL Server..."

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Start the application
echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000