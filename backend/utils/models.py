import os
from sqlalchemy import (
    Column, Integer, Float, Date, create_engine, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('PG_URI'), echo=True)

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = (UniqueConstraint('order_number'),)
    id = Column(Integer, primary_key=True)
    order_number = Column(Integer)
    price_dollars = Column(Float)
    price_rub = Column(Float)
    delivery_time = Column(Date)

    def __init__(
        self,
        order_number,
        price_dollars,
        price_rub,
        delivery_time
    ):
        self.order_number = order_number
        self.price_dollars = price_dollars
        self.price_rub = price_rub
        self.delivery_time = delivery_time

    def __repr__(self):
        return "<Order('%s')>" % (self.order_number)
