#!/bin/sh
set -e

echo "Waiting for PostgreSQL to be ready..."

# export PGPASSWORD so pg_isready can use it
export PGPASSWORD="$POSTGRES_PASSWORD"

until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
  echo "PostgreSQL not ready yet, waiting..."
  sleep 2
done

echo "PostgreSQL is ready!"

echo "Waiting for Redis to be ready..."

until redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping | grep -q PONG; do
  echo "Redis not ready yet, waiting..."
  sleep 2
done

echo "Redis is ready!"

echo "Starting application..."
exec "$@"
