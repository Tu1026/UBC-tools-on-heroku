import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

# redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.Redis.from_url(os.environ.get("REDIS_URL") or 'redis://')
# conn = redis.Redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()