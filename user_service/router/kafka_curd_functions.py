from sqlmodel import Session
from schemas.models import User


def add_new_user(user_data: User, session: Session):
    try:
        print("Adding user to Database")  # Keep this for now
        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        return True  # Indicate success
    except Exception as e:
        print(f"Error adding user: {e}")  # Keep this for now
        session.rollback()  # Rollback the transaction in case of error
        return False  # Indicate failure
