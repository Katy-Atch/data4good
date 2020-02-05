#!/bin/bash
# python manage.py runserver 0.0.0.0:8000
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
gunicorn --workers=2 --bind=0.0.0.0:8000 data4good.wsgi:application