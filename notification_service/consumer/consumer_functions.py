import logging
from notification import setting
from schemas import notification_pb2
from aiokafka import AIOKafkaConsumer
from schemas.model import Notification
from notification.db import get_session
from schemas.schema_registry import protobuf_deserializer
from router.kafka_curd_functions import add_new_notification
from confluent_kafka.serialization import SerializationContext, MessageField, StringDeserializer

logger = logging.getLogger(__name__)  # Configure logging appropriately
string_deserializer = StringDeserializer('utf8')


async def consume_notification_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="notification-group",
        auto_offset_reset="latest",
        key_deserializer=lambda v: string_deserializer(v),
        value_deserializer=lambda v: protobuf_deserializer(
            v, SerializationContext(setting.KAFKA_NOTIFICATION_TOPIC, MessageField.VALUE))
    )

    await consumer.start()
    try:
        async for message in consumer:
            logger.info(f"Message value in Consumer: {message.value}")
            # Parse Protobuf message
            notification_data = message.value
            # enums
            notification_status = notification_pb2.NotificationStatus.Name(
                notification_data.notification_status)
            notification_type = notification_pb2.NotificationType.Name(
                notification_data.notification_type)
            event = notification_pb2.Event.Name(notification_data.event)
            notification_dict = {
                "created_at": notification_data.created_at,
                "username": notification_data.username,
                "contact": notification_data.contact,
                "address": notification_data.address,
                "email": notification_data.email,
                "notification_type": notification_type,
                "event": event,
                "subject": notification_data.subject,
                "message": notification_data.message,
                "notification_status": notification_status,
                "sent_at": notification_data.sent_at,
            }
        # Add to database
        with next(get_session()) as session:
            logger.info("Data received by consumer")
            add_new_notification(
                notification_data=Notification(**notification_dict), session=session)
    except Exception as e:
        logger.error(f"Error processing message in Consumer: {e}")
    finally:
        await consumer.stop()
