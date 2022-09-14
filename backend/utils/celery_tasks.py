import os
import sys
import requests
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

utils_dir = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
sys.path.append(utils_dir)

import logger
import docs_script
import db


load_dotenv()

logger = logger.Logger('celery_tasks', 'celery_tasks').get_logger()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

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
    """Функция Celery для автоматического пополнения БД из GoogleSheets"""
    docs_script.get_new_data_to_db()

@app.task(name='utils.celery_tasks.auto_get_orders_missed_delivery')
def auto_get_orders_missed_delivery():
    """Функция Celery для проверки просроченных заказов и отправка их в телеграмм через бота"""
    missed_orders = [f"""Просроченный заказ:
    Номер заказа: {order.order_number}
    Цена$: {order.price_dollars}
    ЦенаRUB: {order.price_rub}
    Дата поставки: {order.delivery_time.strftime('%d.%m.%Y')}\n""" for order in db.get_orders_missed_delivery_date()
    ]
    if len(missed_orders) > 0:
        for message in missed_orders:
            requests.get(
                f'https://api.telegram.org/{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}'
            )
            logger.info(message)



app.autodiscover_tasks()

app.conf.beat_schedule = { 
    'get_data_by_googleapi_every': { # Запуск обновления из GoogleDocs каждые 30 секунд
        'task': 'utils.celery_tasks.auto_get_data',
        'schedule': 30.0,
    },
    'get_orders_missed_delivery_every_day' : { # Запуск проверки пропущенных сроков поставки каждый полдень
        'task': 'utils.celery_tasks.auto_get_orders_missed_delivery',
        'schedule': crontab(minute=0, hour=12)
    },
}
