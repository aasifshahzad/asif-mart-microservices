import logging
from aiokafka import AIOKafkaConsumer
from confluent_kafka.serialization import SerializationContext, MessageField, StringDeserializer
from inventory.db import get_session
from schemas.model import Inventory
from schemas.schema_registry import protobuf_deserializer
from router.kafka_curd_functions import add_new_inventory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

string_deserializer = StringDeserializer('utf8')


async def consume_inventory_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="inventory-group",
        auto_offset_reset="latest",
        key_deserializer=lambda v: string_deserializer(v),
        value_deserializer=lambda v: protobuf_deserializer(
            v, SerializationContext(topic, MessageField.VALUE))
    )

    await consumer.start()
    try:
        async for message in consumer:
            logger.info(f"Received message on topic {message.topic}")
            inventory_data = message.value

            if not inventory_data:
                logger.error("Received empty inventory data")
                continue

            try:
                inventory_dict = {
                    "id": inventory_data.id,
                    "created_at": inventory_data.created_at,
                    "updated_at": inventory_data.updated_at,
                    "product_name": inventory_data.product_name,
                    "stock_level": inventory_data.stock_level,

                }
                with next(get_session()) as session:
                    add_new_inventory(
                        inventory_data=Inventory(**inventory_dict), session=session)
                logger.info(
                    f"Inventory {inventory_data.name} added to the database.")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped.")
