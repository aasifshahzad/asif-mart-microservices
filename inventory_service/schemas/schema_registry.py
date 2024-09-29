from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from inventory import setting
from schemas.inventory_pb2 import Inventory

# Schema Registry configuration
schema_registry_conf = {'url': setting.SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Protobuf Serializer
protobuf_serializer = ProtobufSerializer(
    Inventory, schema_registry_client, {'use.deprecated.format': False}
)

# Protobuf Deserializer
protobuf_deserializer = ProtobufDeserializer(
    Inventory, {'use.deprecated.format': False})
