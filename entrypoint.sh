#!/bin/sh

cd /app
python manage.py loaddata telecoms area_codes
supervisord -c /app/supervisord.conf
