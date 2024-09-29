import asyncio
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Field, create_engine, select, Session
from typing import Optional, Annotated
from contextlib import asynccontextmanager
from consumer.consumer import consume_user_messages
from user import setting
from user.auth import authenticate_user, create_access_token, create_refresh_token, validate_refresh_token, EXPIRY_TIME
from user.db import create_db_and_tables, engine, get_session
from schemas.models import Token, User
from router import user


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Application")

    # Create database and tables
    create_db_and_tables()
    print("Database and tables created")

    # Create the consumer tasks
    consumer_task = asyncio.create_task(consume_user_messages(
        setting.KAFKA_USER_TOPIC, 'broker:19092'))
    print("Kafka consumer task created")

    try:
        # Ensure the consumer has started
        await asyncio.sleep(0)
        yield

    finally:
        # Gracefully shutdown the consumer tasks
        print("Shutting down consumer task")
        consumer_task.cancel()

        # Wait for the tasks to complete before exiting
        await asyncio.gather(consumer_task, return_exceptions=True)

        print("Application shutdown complete")

app: FastAPI = FastAPI(
    lifespan=lifespan,
    title="User Service App",
    description="A simple User CRUD application",
    version="1.0.0",
)

app.include_router(router=user.user_router)


@app.get("/", tags=["Main"])
async def root():

    return {"Message": "User App running :-}"}


@app.post('/login', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: Annotated[Session, Depends(get_session)]):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    expire_time = timedelta(minutes=EXPIRY_TIME)
    access_token = create_access_token(
        {"sub": form_data.username}, expire_time)

    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token(
        {"sub": user.email}, refresh_expire_time)

    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)


@app.post("/login/refresh")
def refresh_token(old_refresh_token: str,
                  session: Annotated[Session, Depends(get_session)]):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"}
    )

    user = validate_refresh_token(old_refresh_token,
                                  session)
    if not user:
        raise credential_exception

    expire_time = timedelta(minutes=EXPIRY_TIME)
    access_token = create_access_token({"sub": user.username}, expire_time)

    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token(
        {"sub": user.email}, refresh_expire_time)

    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)
