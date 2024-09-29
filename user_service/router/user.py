import datetime
from typing import Annotated
from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, HTTPException
from requests import session
from sqlmodel import Session

from producer.producer import get_kafka_producer
from user import setting
from user.auth import current_user, get_user_from_db, hash_password
from user.db import get_session
from schemas.models import Register_User, User
from schemas.user_pb2 import User as user_proto


user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/")
async def get_users():
    return {"Message": "User Page running :-}"}


@user_router.post("/register")
async def register_user(new_user: Register_User,
                        producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
                        session: Annotated[Session, Depends(get_session)]):

    db_user = get_user_from_db(session, new_user.username, new_user.email)
    if db_user:
        raise HTTPException(
            status_code=409, detail="User with these credentials already exists")
    user_pro = user_proto(
        created_at=int(datetime.datetime.now().timestamp()),
        username=new_user.username,
        email=new_user.email,
        password=hash_password(new_user.password)
    )
    try:
        await producer.send_and_wait(setting.KAFKA_USER_TOPIC, user_pro)
    except Exception as e:
        print(f"Error while sending order to Kafka: {e}")
        raise HTTPException(
            status_code=500, detail="Error while producing message to Kafka")
    return {"message": "New User Created Successfully"}


@user_router.get('/me')
async def user_profile(current_user: Annotated[User, Depends(current_user)]):

    return current_user
