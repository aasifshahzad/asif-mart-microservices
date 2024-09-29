import datetime
from typing import List, Annotated
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel

from inventory import setting
from producer.producer import get_kafka_producer
from schemas.model import Inventory, InventoryCreate, InventoryUpdate, InventoryResponse
from inventory.db import get_session
import requests
from schemas.inventory_pb2 import Inventory as Inventory_proto


inventory_router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
    responses={404: {"description": "Not found"}}
)

# Helper function to fetch product details


@inventory_router.get("/", tags=["Inventory"])
async def root():

    return {"Message": "Inventory Page running :-}"}


def get_product_details(product_name: str):
    # product service route..
    response = requests.get(f"http://product:8000/product/{product_name}")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")
    return response.json()


# Get inventory item by product Name
@inventory_router.get("/get-stock/{product_name}", response_model=InventoryResponse)
async def get_inventory_by_product_name(product_name: str, session: Annotated[Session, Depends(get_session)]):
    inventory_item = session.exec(select(Inventory).where(
        Inventory.product_name == product_name)).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return inventory_item


# List all inventory items
@inventory_router.get("/all-inventory/", response_model=List[InventoryResponse])
async def list_inventory(session: Annotated[Session, Depends(get_session)]):
    inventory_items = session.exec(select(Inventory)).all()
    return inventory_items

# Add new inventory item


@inventory_router.post("/add-stock/", response_model=InventoryResponse)
async def add_inventory_item(inventory: InventoryCreate, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    # Validate product existence
    product = get_product_details(inventory.product_name)
    if not product:
        raise HTTPException(status_code=400, detail="Invalid product Name")

    inventory_proto = Inventory_proto(
        created_at=int(datetime.datetime.now().timestamp()),
        updated_at=int(datetime.datetime.now().timestamp()),
        product_name=inventory.product_name,
        stock_level=inventory.stock_level,
    )
    try:
        await producer.send_and_wait(setting.KAFKA_INVENTORY_TOPIC, inventory_proto)
    except Exception as e:
        print(f"Error while sending order to Kafka: {e}")
        raise HTTPException(
            status_code=500, detail="Error while producing message to Kafka")
    return inventory


# Update inventory item
@inventory_router.patch("/patch-stock/{product_name}", response_model=InventoryResponse)
async def update_inventory_item(
    product_name: str,
    inventory: InventoryUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    inventory_item = session.exec(select(Inventory).where(
        Inventory.product_name == product_name)).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    inventory_data = inventory.model_dump(exclude_unset=True)
    for key, value in inventory_data.items():
        setattr(inventory_item, key, value)

    session.add(inventory_item)
    session.commit()
    session.refresh(inventory_item)
    return inventory_item


# Delete inventory item
@inventory_router.delete("/del-stock/{product_name}")
async def delete_inventory_item(product_name: str, session: Annotated[Session, Depends(get_session)]):
    inventory_item = session.exec(select(Inventory).where(
        Inventory.product_name == product_name)).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    session.delete(inventory_item)
    session.commit()
    return {"message": "Inventory item deleted successfully"}
