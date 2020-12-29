web: flask db upgrade; flask translate compile; gunicorn server:app
worker: rq worker -u $REDIS_URL course-update
heroku ps:scale web=1 worker=20