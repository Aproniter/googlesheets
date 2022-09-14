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

try:
    from models import Order
    from logger import Logger
except ModuleNotFoundError:
    from .models import Order
    from .logger import Logger

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
        s.add_all(new_orders)
        if len(s.new) == 0:
            return
        s.commit()
        return True
    except sqlalchemy.exc.IntegrityError as e:
        logger.error('Ошибка БД', exc_info=True)
        return False


def get_all_orders() -> list:
    """Функция получения всех данных из БД.
    Возвращает список объектов."""
    try:
        s = Session()
        results = s.query(Order).order_by(Order.delivery_time).all()
        return results
    except sqlalchemy.exc.DatabaseError:
        logger.error('Ошибка БД', exc_info=True)


def get_orders_limit(limit) -> list:
    """Функция получения ограниченного
    количества записей."""
    try:
        s = Session()
        results = s.query(Order).order_by(
            Order.delivery_time
        ).limit(limit)
        return results
    except sqlalchemy.exc.DatabaseError:
        logger.error('Ошибка БД', exc_info=True)


def get_orders_missed_delivery_date() -> list:
    """Функция получения из БД заказов с прошедшей
    датой поставки. Возвращает список объектов."""
    try:
        date = datetime.now()
        s = Session()
        results = s.query(Order).filter(
            Order.delivery_time < date
        ).order_by(Order.delivery_time)
        return results
    except sqlalchemy.exc.DatabaseError:
        logger.error('Ошибка БД', exc_info=True)


def get_order_by_order_number(order_number):
    """Функция получения из БД заказа по order_number"""
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
    """Функция удаления из БД заказа по order_number"""
    try:
        s = Session()
        s.query(Order).filter(Order.order_number == order_number).delete()
        s.commit()
        return True
    except sqlalchemy.exc.DatabaseError:
        logger.error('Ошибка БД', exc_info=True)
        return False


if __name__ =='__main__':
    for i in get_orders_missed_delivery_date():
        print(i.order_number, i.price_dollars, i.price_rub, i.delivery_time)
