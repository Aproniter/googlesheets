import os
import sys
import requests
import json
import xmltodict
import redis

from datetime import datetime
from dotenv import load_dotenv

utils_dir = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
sys.path.append(utils_dir)

from logger import Logger
from sheets_script import SheetsHelper
import db

load_dotenv()
logger = Logger('docs_script', 'docs_script').get_logger()


redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT')
)


def get_rate():
    if redis_client.exists('rate'):
        return float(redis_client.get('rate'))
    res = requests.get('https://cbr.ru/scripts/XML_daily.asp')
    try:
        new_rate = float([
            i for i in xmltodict.parse(res.content)['ValCurs']['Valute']
            if i['@ID'] == 'R01235'
            ][0]['Value'].replace(',','.')
        )
        redis_client.set('rate', new_rate, 60*60)
        return new_rate
    except Exception:
        logger.error('Ошибка получения нового курса.', exc_info=True)


def get_new_data():
    sheets_helper = SheetsHelper()
    ws = sheets_helper.get_worksheet()
    print(ws.get_all_records())

def get_new_data_to_db():
    sheets_helper = SheetsHelper()
    ws = sheets_helper.get_worksheet()
    data = ws.get_all_records()
    dollars_rate = get_rate()
    if db.add_orders(
        ({
            'order_number': order['заказ №'],
            'price_dollars': order['стоимость,$'],
            'price_rub': round(order['стоимость,$'] * dollars_rate, 2),
            'delivery_time': order['срок поставки']
        } for order in data)
    ):
        logger.info('Новые данные добавлены в БД.')


if __name__ == '__main__':
    print(get_rate())