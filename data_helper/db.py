import sys
import os
import psycopg2
from psycopg2.extras import execute_values

from datetime import datetime
from dotenv import load_dotenv

logger_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/logger/')

sys.path.append(logger_dir)

from logger import Logger

load_dotenv()
logger = Logger(__name__, 'db').get_logger()


class DbHelper:
    """Класс для работы с базой данных
    При инициализации принимает парметры подключения к БД"""

    def __init__(
        self,
        host=os.getenv('PG_HOST'),
        port=os.getenv('PG_PORT'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASS'),
        db_name=os.getenv('PG_DB'),
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name

    def _get_connect(self):
        return psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            port=self.port,
            host=self.host
        )

    def get_all_data(self):
        """Функция получения всех данных из таблицы заказов"""
        try:
            conn = self._get_connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM orders')
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception:
            logger.error('Ошибка БД', exc_info=True)
            return False

    def insert_data(self, data:tuple):
        """Функция добавления заказа в БД. Приинимает кортеж словарей:
        ({order_number, price_dollars, price_rub, delivery_time})"""
        try:
            conn = self._get_connect()
            cursor = conn.cursor()
            execute_values(
                cursor,
                'INSERT INTO orders (order_number, price_dollars, price_rub, delivery_time) VALUES %s',
                (
                    (i['order_number'], i['price_dollars'], i['price_rub'], i['delivery_time']) 
                    for i in data
                )
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            logger.error('Ошибка БД', exc_info=True)
            return False



# def insert_data(self, data:dict):
#         """Функция добавления заказа в БД. Приинимает словарь:
#         {order_number, price_dollars, price_rub, delivery_time}"""
#         try:
#             conn = self._get_connect()
#             cursor = conn.cursor()
#             cursor.execute(
#                 'INSERT INTO orders (order_number, price_dollars, price_rub, delivery_time) VALUES(%s, %s, %s, %s)',
#                 (data['order_number'], data['price_dollars'], data['price_rub'], data['delivery_time'],)
#             )
#             conn.commit()
#             cursor.close()
#             conn.close()
#             return True
#         except Exception:
#             logger.error('Ошибка БД', exc_info=True)
#             return False


    def delete_data(self, order_number:int):
        """Функция удаления заказа из БД. Приинимает номер заказа"""
        try:
            conn = self._get_connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE order_number = %s", (order_number,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            logger.error('Ошибка БД', exc_info=True)
            return False


if __name__ == '__main__':
    db = DbHelper()
    # db.insert_data({
    #     'order_number': 1,
    #     'price_dollars': 1,
    #     'price_rub': 60,
    #     'delivery_time': datetime.now().strftime('%d/%m/%Y')
    # })
    db.delete_data(1)
    print(db.get_all_data())