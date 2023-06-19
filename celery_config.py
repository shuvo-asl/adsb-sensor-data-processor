from celery import Celery
from time import sleep
celery_app = Celery(
    ['tasks'],
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def process_task(task):
    for i in range(10):
        print(i)
        sleep(1)
    return "Task processed successfully"