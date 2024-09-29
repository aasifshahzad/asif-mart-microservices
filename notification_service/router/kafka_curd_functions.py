from sqlmodel import Session
from datetime import datetime
from schemas.model import Notification
import logging

logger = logging.getLogger(__name__)


def add_new_notification(notification_data: Notification, session: Session):
    try:
        print("Adding notification to Database")  # Keep this for now
        notification_data.created_at = datetime.fromtimestamp(
            notification_data.created_at)
        session.add(notification_data)
        session.commit()
        session.refresh(notification_data)
        logger.info("Notification added successfully")
        return True  # Indicate success
    except Exception as e:
        logger.error(f"Error adding notification to database: {e}")
        session.rollback()  # Rollback the transaction in case of error
        return False  # Indicate failure
