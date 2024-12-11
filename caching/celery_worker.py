from celery_broker import celery_app
from task import heavy_task_prime
import time


@celery_app.task
def check_prime(time_delay: int) -> float:
    
    start = time.time()
    heavy_task_prime(time_delay)
    end = time.time() - start
    
    return end