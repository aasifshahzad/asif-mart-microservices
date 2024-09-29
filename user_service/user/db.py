from sqlmodel import SQLModel, create_engine, Session
from user import setting


CONN_STRING: str = str(setting.DATABASE_URL)


def get_engine(CONN_STRING):
    engine = create_engine(CONN_STRING, echo=True)
    print("Engine created successfully")
    return engine


engine = get_engine(CONN_STRING=CONN_STRING)  # small error in db file


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("Database and tables created successfully")


def get_session():
    with Session(engine) as session:
        yield session


def get_session_override():
    CONN_STRING: str = str(setting.TEST_DATABASE_URL)
    engine = create_engine(CONN_STRING, echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
