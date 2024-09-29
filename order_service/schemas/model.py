from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship, Enum
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, String
import enum


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class OrderBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


class Order(OrderBase, table=True):
    username: str
    email: str
    product_name: str
    quantity: int
    price: float
    status: OrderStatus = Field(default=OrderStatus.PENDING)


class OrderCreate(SQLModel):
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    username: str
    email: str
    product_name: str
    quantity: int
    price: float
    status: OrderStatus = Field(default=OrderStatus.PENDING)


class OrderResponse (OrderBase):
    username: str
    email: str
    product_name: str
    quantity: int
    price: float
    status: OrderStatus


class OrderedItems(SQLModel):
    product_name: str = Field(nullable=False)
    quantity: int = Field(nullable=False)
    price: float
    total_price: float
