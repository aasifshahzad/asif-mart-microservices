from sqlmodel import Session
from schemas.model import Product


def add_new_product(product_data: Product, session: Session):
    try:
        print("Adding order to Database")  # Keep this for now
        session.add(product_data)
        session.commit()
        session.refresh(product_data)
        return True  # Indicate success
    except Exception as e:
        print(f"Error adding order: {e}")  # Keep this for now
        session.rollback()  # Rollback the transaction in case of error
        return False  # Indicate failure
