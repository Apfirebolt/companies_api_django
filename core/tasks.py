from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def example_task(param1, param2):
    logger.info(f"Executing example_task with {param1}, {param2}")
    result = param1 + param2
    print(f"Example Task Result: {result}")
    return result