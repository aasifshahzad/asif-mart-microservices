import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from consumer.consumer_functions import consume_product_messages
from product import setting
from product.db import create_db_and_tables
from router import product


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Application")

    # Create database and tables
    try:
        create_db_and_tables()
        print("Database and tables created")
    except Exception as e:
        print(f"Error creating database and tables: {e}")
        raise

    # Create the consumer task
    consumer_task = None
    try:
        consumer_task = asyncio.create_task(
            consume_product_messages(
                "product-events", 'broker:19092'
            )
        )
        print("Kafka consumer task created")

        # Give the consumer time to start properly
        await asyncio.sleep(1)
        yield

    except Exception as e:
        print(f"Error during application startup or execution: {e}")
        raise

    finally:
        # Gracefully shutdown the consumer task
        if consumer_task:
            print("Shutting down consumer task")
            consumer_task.cancel()

            try:
                await consumer_task
                print("Consumer task shut down successfully")
            except asyncio.CancelledError:
                print("Consumer task was cancelled")

        print("Application shutdown complete")

app: FastAPI = FastAPI(
    lifespan=lifespan,
    title="Product Service App",
    description="A simple User CRUD application",
    version="1.0.0",
)

app.include_router(router=product.product_router)


@app.get("/", tags=["Main"])
async def root():

    return {"Message": "Product App running :-}"}
