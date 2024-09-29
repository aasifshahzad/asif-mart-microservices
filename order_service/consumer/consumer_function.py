
import logging
from order import setting
from schemas import order_pb2
from order.db import get_session
from fastapi import HTTPException
from aiokafka import AIOKafkaConsumer
from confluent_kafka.serialization import SerializationContext, MessageField, StringSerializer, StringDeserializer
from schemas.schema_registry import protobuf_serializer, protobuf_deserializer
from router.kafka_curd_functions import add_new_order
from schemas.model import Order, OrderStatus


logger = logging.getLogger(__name__)  # Configure logging appropriately
string_deserializer = StringDeserializer('utf8')


async def consume_order_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="order-group",
        auto_offset_reset="latest",
        key_deserializer=lambda v: string_deserializer(v),
        value_deserializer=lambda v: protobuf_deserializer(
            v, SerializationContext(setting.KAFKA_ORDER_TOPIC, MessageField.VALUE))
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")
            print(f"Message value: {message.value}")
            order_data = message.value
            status_name = order_pb2.OrderStatus.Name(order_data.status)
            order_dict = {
                "id": order_data.id,
                "created_at": order_data.created_at,
                "updated_at": order_data.updated_at,
                "username": order_data.username,
                "email": order_data.email,
                "product_name": order_data.product_name,
                "quantity": order_data.quantity,
                "price": order_data.price,
                "status": OrderStatus[status_name],
            }

            with next(get_session()) as session:
                print("Data received by consumer")
                add_new_order(
                    order_data=Order(**order_dict), session=session)
    except Exception as e:
        logger.error(f"Error processing message in Consumer: {e}")
    finally:
        await consumer.stop()
