from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color = Column(String)
    logo = Column(String)
    rating = Column(Float)
    reviews = Column(Integer)
    address = Column(String)
    coords_x = Column(Float)  # Posición X porcentual en el mapa (0-100)
    coords_y = Column(Float)  # Posición Y porcentual en el mapa (0-100)
    hours = Column(String)
    delivery_fee = Column(Float)
    min_delivery_time = Column(String)

    # Relación con las ofertas de productos
    offers = relationship("StoreProductAssociation", back_populates="store", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    category = Column(String, index=True)
    description = Column(Text)
    icon = Column(String)
    specs = Column(JSON)  # Almacena especificaciones técnicas como JSON

    # Relación con las ofertas de tiendas
    offers = relationship("StoreProductAssociation", back_populates="product", cascade="all, delete-orphan")


class StoreProductAssociation(Base):
    __tablename__ = "store_products"

    store_id = Column(String, ForeignKey("stores.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    delivery_time = Column(String)

    store = relationship("Store", back_populates="offers")
    product = relationship("Product", back_populates="offers")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    subtotal = Column(Float, nullable=False)
    shipping_fee = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    store_id = Column(String, nullable=False)
    store_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(String, nullable=False)  # Maestro de Obra, Cliente General, Transportista
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

