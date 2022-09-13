import os
import sys
from celery import Celery
from dotenv import load_dotenv

utils_dir = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
sys.path.append(utils_dir)

import logger
import docs_script


load_dotenv()

logger = logger.Logger('celery_tasks', 'celery_tasks').get_logger()

app = Celery('celery_task')

app.conf.update(
    result_expires=60,
    task_acks_late=True,
    timezone='UTC',
    broker_url=os.getenv('CELERY_BROKER_URL'),
    result_backend=os.getenv('CELERY_RESULT_BACKEND'),
)

@app.task(name='utils.celery_tasks.auto_get_data')
def auto_get_data():
    docs_script.get_new_data_to_db()

    
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get_data_by_googleapi_every': {
        'task': 'utils.celery_tasks.auto_get_data',
        'schedule': 30.0,
    },
}