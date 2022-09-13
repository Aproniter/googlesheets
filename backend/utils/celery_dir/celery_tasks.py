import os
import sys
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

logger_dir = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
sys.path.append(logger_dir)
from logger import Logger


load_dotenv()

logger = Logger('celery_tasks', 'celery_tasks').get_logger()

app = Celery('celery_task')

app.conf.update(
    result_expires=60,
    task_acks_late=True,
    timezone='UTC',
    broker_url=os.getenv('CELERY_BROKER_URL'),
    result_backend=os.getenv('CELERY_RESULT_BACKEND'),
)


@app.task(name='utils.celery_dir.celery_tasks.test')
def test():
    logger.error('test task')

@app.task(name='utils.celery_dir.celery_tasks.auto_test')
def auto_test():
    logger.error('auto_test task')

    
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'utils.celery_dir.celery_tasks.auto_test',
        # 'schedule': crontab(),
        'schedule': 10.0,
    },
}