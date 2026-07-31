#!/bin/sh

echo "Waiting for PostgreSQL..."

sleep 20

echo "Creating database tables..."
python -m database.init_db

echo "Running ETL..."
python -m loading.upsert_users