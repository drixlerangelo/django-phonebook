#!/bin/sh

cd /app
# Since I set a custom user model, I'll need to do this
# Reference: https://stackoverflow.com/a/48476148
sed -i "s|'django.contrib.admin'|#'django.contrib.admin'|g" app/settings.py
sed -i "s|path('admin/', admin.site.urls)|#path('admin/', admin.site.urls)|g" app/urls.py
python manage.py migrate
sed -i "s|#'django.contrib.admin'|'django.contrib.admin'|g" app/settings.py
sed -i "s|#path('admin/', admin.site.urls)|path('admin/', admin.site.urls)|g" app/urls.py
python manage.py migrate
python manage.py loaddata telecoms area_codes
supervisord -c /app/supervisord.conf
