from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from schemas.notification_pb2 import Notification

schema_registry_conf = {'url': "http://schema-registry:8081"}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Protobuf Serializer
protobuf_serializer = ProtobufSerializer(
    Notification, schema_registry_client, {
        'use.deprecated.format': False}
)

# Protobuf Deserializer
protobuf_deserializer = ProtobufDeserializer(
    Notification, {'use.deprecated.format': False}
)
