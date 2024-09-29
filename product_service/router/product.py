import datetime
from typing import Annotated
from aiokafka import AIOKafkaProducer
from fastapi import File, UploadFile
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
import os
from sqlmodel import Session, select
from producer.producer_functions import get_kafka_producer
from product import setting
from product.db import get_session
from schemas.model import Product, ProductCreate,  ProductResponse, ProductUpdate
from schemas.product_pb2 import Product as ProductProto


product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    responses={404: {"description": "Not found"}}
)


IMAGEDIR = "images/"


@product_router.get("/")
async def get_product():
    return {"Message": "Product page running :-}"}

# Image upload and show


@product_router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):

    if not os.path.exists(IMAGEDIR):
        os.makedirs(IMAGEDIR)

    file_path = os.path.join(IMAGEDIR, file.filename)
    contents = await file.read()

    # save the file
    with open(file_path, "wb") as f:
        f.write(contents)

    return {"filename": file.filename}


@product_router.get("/show/{file_name}")
async def read_file(file_name: str):
    path = os.path.join(IMAGEDIR, file_name)
    if not os.path.exists(IMAGEDIR):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)


@product_router.get("/product_list", response_model=list[ProductResponse] | None)
async def all_products(session: Annotated[Session, Depends(get_session)]):
    products = session.exec(select(Product)).all()
    return products


@product_router.post("/add_product", response_model=ProductResponse)
async def add_product(product: ProductCreate, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    product_proto = ProductProto(
        created_at=int(datetime.datetime.now().timestamp()),
        updated_at=int(datetime.datetime.now().timestamp()),
        name=product.name,
        description=product.description,
        category=product.category,
        cost_price=product.cost_price,
        sale_price=product.sale_price,
        discount=product.discount,
    )
    try:
        await producer.send_and_wait(setting.KAFKA_PRODUCT_TOPIC, product_proto)
    except Exception as e:
        print(f"Error while sending order to Kafka: {e}")
        raise HTTPException(
            status_code=500, detail="Error while producing message to Kafka")
    return product


@product_router.get("/{product_name}", response_model=ProductResponse | None)
async def get_product_by_name(product_name: str, session: Annotated[Session, Depends(get_session)]):
    product = session.exec(select(Product).where(
        Product.name == product_name)).first()
    if product:
        return product
    else:
        return None


@product_router.patch("/patch/{product_name}", response_model=ProductResponse)
async def update_product(
    product_name: str,
    product: ProductUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    existing_product = session.exec(
        select(Product).where(Product.name == product_name)).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_dict_data = product.model_dump(exclude_unset=True)
    for key, value in product_dict_data.items():
        setattr(existing_product, key, value)

    session.add(existing_product)
    session.commit()
    session.refresh(existing_product)
    return existing_product


@product_router.delete("/del/{product_name}")
async def product_delete(session: Annotated[Session, Depends(get_session)], product_name: str):
    product = session.exec(select(Product).where(
        Product.name == product_name)).first()
    if product:
        session.delete(product)
        session.commit()
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
