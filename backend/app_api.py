from flask import Flask
from flask_restful import Api, Resource, reqparse

from dotenv import load_dotenv

from .utils import db, models, docs_script
from .utils.logger import Logger

load_dotenv()
logger = Logger('main_api', 'main_api').get_logger()

app = Flask(__name__)
api = Api(app)


class Oreder(Resource):
    """Класс работы с заказами из API"""

    def get(self, id=0):
        if id == 0:
            orders = db.get_all_orders() 
            return orders, 200
        # for quote in ai_quotes:
        #     if(quote["id"] == id):
        #         return quote, 200
        return "Quote not found", 404