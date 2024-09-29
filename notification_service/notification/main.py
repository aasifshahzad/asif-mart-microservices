import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from notification.db import create_db_and_tables
from consumer.consumer_functions import consume_notification_messages
from router.notification import notification_router


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
            consume_notification_messages(
                'notification-events', 'broker:19092')  # type: ignore
        )
        print("Kafka consumer task created")

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
    title="Notification Service App",
    description="A simple Notification CRUD application",
    version="1.0.0",
)


app.include_router(router=notification_router)


@app.get("/", tags=["Main"])
async def root():
    return {"Message": "Notification App running :-}"}
