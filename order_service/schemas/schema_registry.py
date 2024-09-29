from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from order import setting
from schemas.order_pb2 import Order

# Schema Registry configuration
# schema_registry_conf = {'url': setting.SCHEMA_REGISTRY_URL}
schema_registry_conf = {'url': 'http://schema-registry:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Protobuf Serializer
protobuf_serializer = ProtobufSerializer(
    Order, schema_registry_client, {'use.deprecated.format': False}
)

# Protobuf Deserializer
protobuf_deserializer = ProtobufDeserializer(
    Order, {'use.deprecated.format': False}
)
