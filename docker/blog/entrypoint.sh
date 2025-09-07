#!/bin/sh
./wait-for-postgres.sh db
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8000