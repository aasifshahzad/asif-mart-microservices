import logging
from aiokafka import AIOKafkaConsumer
from confluent_kafka.serialization import SerializationContext, MessageField, StringDeserializer
from product.db import get_session
from schemas.model import Product
from schemas.schema_registry import protobuf_deserializer
from router.kafka_curd_functions import add_new_product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

string_deserializer = StringDeserializer('utf8')


async def consume_product_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product-group",
        auto_offset_reset="latest",
        key_deserializer=lambda v: string_deserializer(v),
        value_deserializer=lambda v: protobuf_deserializer(
            v, SerializationContext(topic, MessageField.VALUE))
    )

    await consumer.start()
    try:
        async for message in consumer:
            logger.info(f"Received message on topic {message.topic}")
            product_data = message.value

            if not product_data:
                logger.error("Received empty product data")
                continue

            try:
                product_dict = {
                    "id": product_data.id,
                    "created_at": product_data.created_at,
                    "updated_at": product_data.updated_at,
                    "name": product_data.name,
                    "description": product_data.description,
                    "category": product_data.category,
                    "cost_price": product_data.cost_price,
                    "sale_price": product_data.sale_price,
                    "discount": product_data.discount
                }
                with next(get_session()) as session:
                    add_new_product(
                        product_data=Product(**product_dict), session=session)
                logger.info(
                    f"Product {product_data.name} added to the database.")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped.")
