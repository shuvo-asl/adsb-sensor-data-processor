# Run Celery worker
celery -A schedule.celery worker --loglevel=INFO --detach --pidfile=''

# Run Celery Beat
celery -A schedule.celery beat --loglevel=INFO --detach --pidfile=''

flask run --host=0.0.0.0 --port 5000