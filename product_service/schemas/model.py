from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from uuid import UUID, uuid4


class ProductBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


class Product(ProductBase, table=True):
    name: str
    description: str
    category: str
    cost_price: float
    sale_price: float
    discount: float


class ProductCreate(SQLModel):
    name: str
    description: str
    category: str
    cost_price: float
    sale_price: float
    discount: float


class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    cost_price: float | None = None
    sale_price: float | None = None
    discount: float | None = None


class ProductResponse(ProductBase):
    name: str
    description: str
    category: str
    cost_price: float
    sale_price: float
    discount: float
