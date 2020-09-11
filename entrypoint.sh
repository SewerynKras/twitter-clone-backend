#!/bin/sh

# Wait for postgres to finish initialing before running any django migrations

echo "Waiting for postgres..."

# these 2 environment variables are set inside the docker-compose file
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"


python manage.py migrate --noinput

exec "$@"