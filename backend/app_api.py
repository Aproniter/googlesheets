import json
from datetime import datetime
import os
import sys

from flask import Flask
from flask_restful import Api, Resource, reqparse

from dotenv import load_dotenv

utils_dir = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
sys.path.append(utils_dir)

import utils
from utils.logger import Logger

load_dotenv()
logger = Logger('main_api', 'main_api').get_logger()

app = Flask(__name__)
api = Api(app)


class Order(Resource):
    """Класс работы с заказами из API"""

    def get(self, order_number=0):
        """Получить все заказы или заказ по order_number"""
        if order_number == 0:
            items_db = utils.db.get_all_orders()
        else:
            items_db = utils.db.get_order_by_order_number(order_number)
        orders = [{
                'order_id': order.id,
                'order_number' : order.order_number,
                'price_dollars' : order.price_dollars,
                'price_rub' : order.price_rub,
                'delivery_time' : order.delivery_time.strftime('%d.%m.%Y')
            } for order in items_db
            ]
        if orders:
            return orders, 200
        logger.warning('Запрос несуществующего заказа.')
        return json.dumps(
            {'error': 'Non-existent order.'}
        ), 404

    def post(self):
        """Ручное добавление заказа"""
        parser = reqparse.RequestParser()
        parser.add_argument('order_number')
        parser.add_argument('price_dollars')
        parser.add_argument('price_rub')
        parser.add_argument('delivery_time')
        params = parser.parse_args()
        data = (
            {
            'order_number': params['order_number'],
            'price_dollars': params['price_dollars'],
            'price_rub': params['price_rub'],
            'delivery_time': params['delivery_time'],
        },
        )
        utils.db.add_orders(data)
        return data, 200

api.add_resource(
    Order, '/orders', '/orders/', '/orders/<int:order_number>'
)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)