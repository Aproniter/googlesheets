import os
import requests
import json
import xmltodict

from datetime import datetime
from dotenv import load_dotenv

import utils.db
from .logger import Logger
# from sheets_script import SheetsHelper

load_dotenv()
logger = Logger('docs_script', 'docs_script').get_logger()
# sheets_helper = SheetsHelper()
# ws = sheets_helper.get_worksheet()


def get_rate():
    res = requests.get('https://cbr.ru/scripts/XML_daily.asp')
    try:
        return float([
                i for i in xmltodict.parse(res.content)['ValCurs']['Valute']
                if i['@ID'] == 'R01235'
            ][0]['Value'].replace(',','.')
        )
    except Exception:
        logger.error('Ошибка получения нового курса.', exc_info=True)


# def get_new_data():
#     print(ws.get_all_records())

# def get_new_data_to_db():
#     data = ws.get_all_records()
#     dollars_rate = get_rate()
#     if db.add_orders(
#         ({
#             'order_number': order['заказ №'],
#             'price_dollars': order['стоимость,$'],
#             'price_rub': round(order['стоимость,$'] * dollars_rate, 2),
#             'delivery_time': order['срок поставки']
#         } for order in data)
#     ):
#         logger.info('Новые данные добавлены в БД.')


if __name__ == '__main__':
    print(get_rate())