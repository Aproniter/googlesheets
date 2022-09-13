import os
import sys
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import literal
from dotenv import load_dotenv
from datetime import datetime

utils_dir = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
sys.path.append(utils_dir)

from models import Order
from logger import Logger

load_dotenv()
logger = Logger('db', 'db').get_logger()

engine = sqlalchemy.create_engine(os.getenv('PG_URI'), echo=False)
Session = sessionmaker(bind=engine)

def add_orders(data:tuple) -> bool:
    """Функция добавления в БД. Принимает кортеж словарей вида
    ({order_number, price_dollars, price_rub, delivery_time},...)
    для записи в базу. Ошибка возвращает False, успех - True"""
    s = Session()
    new_orders = ((Order( # Создаем кортеж объектов БД
        order_number=order['order_number'],
        price_dollars=order['price_dollars'],
        price_rub=order['price_rub'],
        delivery_time=datetime.strptime(order['delivery_time'], '%d.%m.%Y')
    )) for order in data if (
        not s.query(           # Добавляем только объекты с номером заказа, 
        literal(True)).filter( # которых нет в БД
            Order.order_number == order['order_number']
        ).first())
    )
    try:
        if len(new_orders) == 0:
            return
        s.add_all(new_orders)
        s.commit()
        return True
    except sqlalchemy.exc.IntegrityError as e:
        logger.error('Ошибка БД', exc_info=True)
        return False


def get_all_orders() -> list:
    """Функция получения всех данных из БД.
    Возвращает список объектов"""
    try:
        s = Session()
        results = s.query(Order).all()
        return results
    except sqlalchemy.exc.DatabaseError:
        logger.error('Ошибка БД', exc_info=True)


def get_order_by_order_number(order_number):
    try:
        s = Session()
        order = s.query(Order).filter(Order.order_number == order_number)
        if order:
            return order
        return False
    except sqlalchemy.exc.DatabaseError:
        logger.error('Ошибка БД', exc_info=True)
        return False


def delete_order_by_order_number(order_number):
    try:
        s = Session()
        s.query(Order).filter(Order.order_number == order_number).delete()
        s.commit()
        return True
    except sqlalchemy.exc.DatabaseError:
        logger.error('Ошибка БД', exc_info=True)
        return False


if __name__ =='__main__':
    # data = (
    #     {
    #     'order_number': 25,
    #     'price_dollars': round(a := random.randint(600,2000)/3, 2),
    #     'price_rub': round(a * 6.24, 2),
    #     'delivery_time': datetime.now().strftime('%d.%m.%Y')
    # },# for i in range(12, 25)
    # )
    # add_orders(data)
    # delete_order_by_order_number(25)
    for i in get_all_orders():
        print(i.order_number, i.price_dollars, i.price_rub, i.delivery_time)
    