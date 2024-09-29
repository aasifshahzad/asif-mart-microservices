from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class InventoryBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


class Inventory(InventoryBase, table=True):
    product_name: str = Field(nullable=False)
    stock_level: int = Field(default=0, nullable=False)


class InventoryCreate(SQLModel):
    product_name: str
    stock_level: int | None = None


class InventoryUpdate(SQLModel):
    stock_level: int | None = None


class InventoryResponse(InventoryBase):
    product_name: str
    stock_level: int | None
