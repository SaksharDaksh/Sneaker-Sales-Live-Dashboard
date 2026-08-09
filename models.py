from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    brand = Column(String(50))
    category = Column(String(50))       # e.g. Sneakers, Jeans, Hoodies, Shirts
    size = Column(String(10))           # e.g. UK 8, M, L, 32
    price = Column(Numeric(10, 2))


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    region = Column(String(50))
    timestamp = Column(TIMESTAMP, server_default=func.now())
