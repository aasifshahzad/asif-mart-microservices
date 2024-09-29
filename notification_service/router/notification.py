import datetime
from notification import setting
from typing import List, Annotated
from sqlmodel import Session, select
from schemas import notification_pb2
from aiokafka import AIOKafkaProducer
from notification.db import get_session
from fastapi import APIRouter, Depends, HTTPException
from producer.producer_functions import get_kafka_producer
from schemas.notification_pb2 import Notification as NotificationProto
from schemas.model import Notification, NotificationResponse, RecipientInfo, CreateNotification

notification_router = APIRouter(
    prefix="/notification",
    tags=["Notification"],
    responses={404: {"Description": "Not found"}}
)


@notification_router.post("/notify/", response_model=CreateNotification)
async def create_notification(
    recipient_info: RecipientInfo,
    notification: CreateNotification,
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
):
    print("Data get directly in post API is ", recipient_info, notification)
    notification_proto = NotificationProto(
        created_at=int(datetime.datetime.now().timestamp()),
        username=recipient_info.username,
        address=recipient_info.address,
        contact=recipient_info.contact,
        email=recipient_info.email,
        notification_type=notification_pb2.NotificationType.PROMOTIONAL,
        event=notification_pb2.Event.PAYMENT_CONFIRMATION,
        subject=notification.subject,
        message=notification.message,
        notification_status=notification_pb2.NotificationStatus.SENT,
        sent_at=int(datetime.datetime.now().timestamp()),
    )
    try:
        # Log the topic and serialized notification for debugging
        print(f"Sending to topic: {setting.KAFKA_NOTIFICATION_TOPIC}")
        print(f"Serialized notification: {notification_proto}")
        await producer.send_and_wait(setting.KAFKA_NOTIFICATION_TOPIC, notification_proto)
    except Exception as e:
        print(f"Error while sending notification to Kafka: {e}")
        raise HTTPException(
            status_code=500, detail="Error while producing message to Kafka")
    return notification


@notification_router.get("/", response_model=dict)
async def root():
    return {"Message": "Notification page running :-}"}


@notification_router.get("/all/", response_model=List[NotificationResponse])
def read_notifications(session: Session = Depends(get_session)):
    notifications = session.exec(select(Notification)).all()
    return notifications

# Returns notification of any specific notification-id


@notification_router.get("/{id}/", response_model=NotificationResponse)
def read_notification(id: int, session: Session = Depends(get_session)):
    notification = session.get(Notification, id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification
