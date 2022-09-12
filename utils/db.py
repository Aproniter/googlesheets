import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import literal
from datetime import datetime
from dotenv import load_dotenv
import random

from models import Order

load_dotenv()

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
        delivery_time=order['delivery_time']
    )) for order in data if (
        not s.query(           # Добавляем только объекты с номером заказа, 
        literal(True)).filter( # которых нет в БД
            Order.order_number == order['order_number']
        ).first())
    )
    try:
        s.add_all(new_orders)
        s.commit()
        return True
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        return False


def get_all_orders() -> list:
    """Функция получения всех данных из БД.
    Возвращает список объектов"""
    s = Session()
    return s.query(Order).all()


if __name__ =='__main__':
    data = (
        {
        'order_number': 25,
        'price_dollars': round(a := random.randint(600,2000)/3, 2),
        'price_rub': round(a * 6.24, 2),
        'delivery_time': datetime.now().strftime('%d.%m.%Y')
    },# for i in range(12, 25)
    )
    # add_orders(data)
    print(get_all_orders())
    