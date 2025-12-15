#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HSOT $SQL_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL Started"
fi

echo "Building Tailwind CSS..."
python manage.py tailwind install
python manage.py tailwind build

echo "Applying Migrations..."
python manage.py migrate
python manage.py collectstatic --no-input

exec "$@"