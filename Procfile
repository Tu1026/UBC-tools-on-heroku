web: flask db upgrade; gunicorn server:app
worker: rq worker -u $REDIS_URL course-update