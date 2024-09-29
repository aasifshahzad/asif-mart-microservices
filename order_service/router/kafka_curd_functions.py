from sqlmodel import Session
from datetime import datetime
from schemas.model import Order
import logging

logger = logging.getLogger(__name__)


def add_new_order(order_data: Order, session: Session):
    try:
        print("Adding order to Database")  # Keep this for now
        # Convert the Unix timestamp to a datetime object
        order_data.created_at = datetime.fromtimestamp(
            order_data.created_at)
        session.add(order_data)
        session.commit()
        session.refresh(order_data)
        return True  # Indicate success
    except Exception as e:
        logger.error(f"Error adding order to database: {e}")
        session.rollback()  # Rollback the transaction in case of error
        return False  # Indicate failure
