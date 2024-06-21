#!/bin/sh

python ./manage.py migrate
python ./manage.py collectstatic --noinput
exec gunicorn blaastbackend.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 60
