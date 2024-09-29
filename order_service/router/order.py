import datetime
from typing import List, Annotated
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from order import setting
from schemas import order_pb2
from schemas.order_pb2 import Order as OrderCreateProto
from order.db import get_session
from producer.producer_function import get_kafka_producer
from schemas.model import Order, OrderCreate, OrderResponse, OrderStatus, OrderedItems

order_router = APIRouter(
    prefix="/order",
    tags=["Order"],
    responses={404: {"Description": "Not found"}}
)


@order_router.get("/", response_model=dict)
async def root():
    return {"Message": "Order page running :-}"}


@order_router.post("/create-order/", response_model=OrderResponse)
async def create_order(order: OrderCreate, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    print(f"Producer object in create_order: {producer}")
    order_proto = OrderCreateProto(
        created_at=int(datetime.datetime.now().timestamp()),
        updated_at=int(datetime.datetime.now().timestamp()),
        username=order.username,
        email=order.email,
        product_name=order.product_name,
        quantity=order.quantity,
        price=order.price,
        status=order_pb2.OrderStatus.PENDING

    )
    # db_order = Order(**order.model_dump())
    try:
        # Log the topic and serialized order for debugging
        print(f"Sending to topic: {setting.KAFKA_ORDER_TOPIC}")
        print(f"Serialized order: {order_proto}")
        await producer.send_and_wait(setting.KAFKA_ORDER_TOPIC, order_proto)
    except Exception as e:
        print(f"Error while sending order to Kafka: {e}")
        raise HTTPException(
            status_code=500, detail="Error while producing message to Kafka")
    return order


# Returns all placed orders

@order_router.get("/all/", response_model=List[OrderResponse])
def read_orders(session: Session = Depends(get_session)):
    orders = session.exec(select(Order)).all()
    return orders

# Returns order of any specific order-id


@order_router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@order_router.get("/ordered-items/", response_model=List[OrderedItems])
def read_order_items(session: Session = Depends(get_session)):
    order_items = session.exec(select(Order)).all()
    ordered_items_list = []
    for item in order_items:
        total_price = item.quantity * item.price
        ordered_item = OrderedItems(
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price,
            total_price=total_price
        )
        ordered_items_list.append(ordered_item)
    return ordered_items_list


@order_router.delete("/{order_id}", response_model=dict)
def delete_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order)
    session.commit()
    return {"message": "Order deleted successfully"}
