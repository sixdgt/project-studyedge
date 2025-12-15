#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HSOT $SQL_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL Started"
fi

cd /home/studyedge
# --- Auto-create Tailwind theme app if missing ---
if [ ! -d "theme" ]; then
    echo "Creating Tailwind app 'theme'..."
    python manage.py tailwind init --app-name theme --template 1
fi

# Install & build Tailwind CSS
echo "Installing Tailwind CSS..."
python manage.py tailwind install

echo "Building Tailwind CSS..."
python manage.py tailwind build

echo "Applying Migrations..."
python manage.py migrate
python manage.py collectstatic --no-input

exec "$@"