from celery import shared_task


@shared_task(bind=True)
def process_task(self, task):
    print("hello task from tasks file: ", task)
    return "Task processed successfully"