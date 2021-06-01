web: gunicorn dummy.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate
worker: celery -A dummy worker -l info