from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class StoreBase(BaseModel):
    id: str
    name: str
    color: str
    logo: str
    rating: float
    reviews: int
    address: str
    coords_x: float
    coords_y: float
    hours: str
    delivery_fee: float
    min_delivery_time: str

    class Config:
        from_attributes = True

class StoreOfferSchema(BaseModel):
    storeId: str
    price: float
    stock: int
    deliveryTime: str

    class Config:
        from_attributes = True

class ProductSchema(BaseModel):
    id: int
    name: str
    brand: str
    category: str
    description: str
    icon: str
    specs: Dict[str, Any]
    stores: List[StoreOfferSchema]

    class Config:
        from_attributes = True

# Esquemas para la Compra (Checkout)
class CartItemIn(BaseModel):
    productId: int
    storeId: str
    quantity: int
    price: float

class CheckoutIn(BaseModel):
    items: List[CartItemIn]
    district: str


class OrderItemOut(BaseModel):
    productId: int
    productName: str
    storeId: str
    storeName: str
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    createdAt: datetime
    subtotal: float
    shippingFee: float
    total: float
    items: List[OrderItemOut]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    role: str
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

