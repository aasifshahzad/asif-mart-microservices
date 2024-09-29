from fastapi import HTTPException
from aiokafka import AIOKafkaProducer
from schemas.schema_registry import protobuf_serializer
from confluent_kafka.serialization import SerializationContext, MessageField, StringSerializer

string_serializer = StringSerializer('utf8')


async def get_kafka_producer():
    try:
        producer = AIOKafkaProducer(
            bootstrap_servers='broker:19092',
            key_serializer=string_serializer,
            value_serializer=lambda v: protobuf_serializer(
                v,
                SerializationContext(
                    "order-events", MessageField.VALUE)
            )
        )
        await producer.start()
        print("Kafka producer connected successfully")
        yield producer

    except Exception as e:
        print(f"Error connecting to Kafka: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to connect to Kafka")
