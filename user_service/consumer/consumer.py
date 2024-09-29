import logging
from aiokafka import AIOKafkaConsumer
from confluent_kafka.serialization import SerializationContext, MessageField, StringDeserializer
from user.db import get_session
from schemas.models import User
from schemas.schema_registry import protobuf_deserializer
from router.kafka_curd_functions import add_new_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

string_deserializer = StringDeserializer('utf8')


async def consume_user_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="user-group",
        auto_offset_reset="latest",
        key_deserializer=lambda v: string_deserializer(v),
        value_deserializer=lambda v: protobuf_deserializer(
            v, SerializationContext(topic, MessageField.VALUE))
    )

    await consumer.start()
    try:
        async for message in consumer:
            logger.info(f"Received message on topic {message.topic}")
            user_data = message.value

            if not user_data:
                logger.error("Received empty user data")
                continue

            try:
                user_dict = {
                    "id": user_data.id,
                    "created_at": user_data.created_at,
                    "username": user_data.username,
                    "email": user_data.email,
                    "password": user_data.password,

                }
                with next(get_session()) as session:
                    add_new_user(
                        user_data=User(**user_dict), session=session)
                logger.info(
                    f"User {user_data.name} added to the database.")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped.")
