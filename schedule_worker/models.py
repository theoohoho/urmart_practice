from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Order(Base):
    __tablename__ = "dashboard_order"

    order_id = Column(String(100), primary_key=True, index=True)
    product_id = Column(Integer)
    qty = Column(Integer)
    price = Column(Integer)
    shop_id = Column(String(10))
    customer_id = Column(String(50))


class Analytic(Base):
    __tablename__ = "dashboard_analytic"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(String(10))
    total_sales_amount = Column(Integer)
    total_sales_products = Column(Integer)
    total_orders = Column(Integer)
    batch = Column(Integer)
    timestamp = Column(DateTime)
