#!/bin/bash
# python manage.py runserver 0.0.0.0:8000
gunicorn --workers=2 --bind=0.0.0.0:8000 data4good.wsgi:application