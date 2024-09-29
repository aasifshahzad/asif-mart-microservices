from datetime import datetime
from sqlmodel import SQLModel, Field
from fastapi import Form
from typing import Annotated
from typing import Optional


class UserBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(), nullable=False)


class User (UserBase, table=True):
    username: str
    email: str
    password: str


# class Register_User(SQLModel):
#     username: Annotated[
#         str,
#         Form(),
#     ]
#     email:  Annotated[
#         str,
#         Form(),
#     ]
#     password:  Annotated[
#         str,
#         Form(),
#     ]
class Register_User(SQLModel):
    username: str
    email: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenData(SQLModel):
    username: Optional[str] = None


class RefreshToken(SQLModel):
    email: str
