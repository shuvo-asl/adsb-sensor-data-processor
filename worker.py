from rq import Worker, Queue, Connection
from redis import Redis
from app import app

redis_conn = Redis()
listen = ['default']

if __name__ == '__main__':
    with Connection(connection=redis_conn):
        worker = Worker(map(Queue, listen))
        with app.app_context():
            worker.work()
