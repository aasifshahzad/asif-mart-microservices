from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from product import setting
from schemas.product_pb2 import Product

# Schema Registry configuration
# schema_registry_conf = {'url': setting.SCHEMA_REGISTRY_URL}
schema_registry_conf = {'url': 'http://schema-registry:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Protobuf Serializer
protobuf_serializer = ProtobufSerializer(
    Product, schema_registry_client, {'use.deprecated.format': False}
)

# Protobuf Deserializer
protobuf_deserializer = ProtobufDeserializer(
    Product, {'use.deprecated.format': False}
)
