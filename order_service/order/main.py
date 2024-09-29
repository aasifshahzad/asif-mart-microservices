import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Field, create_engine, select, Session
from typing import Optional, Annotated


from datetime import timedelta
from contextlib import asynccontextmanager

from consumer.consumer_function import consume_order_messages
from order import setting
from order.db import create_db_and_tables, engine, get_session

from router.order import order_router


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
            consume_order_messages(setting.KAFKA_ORDER_TOPIC, 'broker:19092')
        )
        print("Kafka consumer task created")

        # Ensure the consumer has started
        # Increased sleep to give the consumer more time to start.
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
    title="Order Service App",
    description="A simple Order CRUD application",
    version="1.0.0",
)


app.include_router(router=order_router)


@app.get("/", tags=["Main"])
async def root():
    return {"Message": "Order App running :-}"}
