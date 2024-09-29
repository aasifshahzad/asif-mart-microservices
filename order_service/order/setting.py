from starlette.config import Config
from starlette.datastructures import Secret

try:
    # config = Config("e:/Cloud/Project-mart/order_service/.env")
    config = Config(".env")

except FileNotFoundError:
    print("No .env file found, using default environment variables")
    config = Config()

DATABASE_URL = config.get("DATABASE_URL", cast=Secret)
TEST_DATABASE_URL = config.get("TEST_DATABASE_URL", cast=Secret)


BOOTSTRAP_SERVER = config.get("BOOTSTRAP_SERVER", cast=str)
KAFKA_ORDER_TOPIC = config.get("KAFKA_ORDER_TOPIC", cast=str)
KAFKA_CONSUMER_GROUP_ID_FOR_ORDER = config.get(
    "KAFKA_CONSUMER_GROUP_ID_FOR_ORDER", cast=str)
SCHEMA_REGISTRY_URL = config.get("SCHEMA_REGISTRY_URL", cast=str)

# Check if important variables are still missing
if not DATABASE_URL or not TEST_DATABASE_URL:
    raise ValueError(
        "Critical configuration is missing: DATABASE_URL or TEST_DATABASE_URL.")
