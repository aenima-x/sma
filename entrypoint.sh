#!/bin/sh

echo "Waiting for postgres"

while ! nc -z db 5432; do
  sleep 0.5
done

echo "Starting app"
python manage.py migrate
python manage.py runserver 0.0.0.0:8000