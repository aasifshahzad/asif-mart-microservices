from sqlmodel import Session
from schemas.model import Inventory


def add_new_inventory(inventory_data: Inventory, session: Session):
    try:
        print("Adding inventory to Database")  # Keep this for now
        session.add(inventory_data)
        session.commit()
        session.refresh(inventory_data)
        return True  # Indicate success
    except Exception as e:
        print(f"Error adding inventory: {e}")  # Keep this for now
        session.rollback()  # Rollback the transaction in case of error
        return False  # Indicate failure
