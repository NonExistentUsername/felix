#!/bin/sh

echo "Waiting for database..."

while ! nc -z db 3306; do
  sleep 0.1
done

echo "Database started"

exec "$@"