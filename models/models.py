from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str 

class Link(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    url: str
    order: int
    click_count: int = 0
    user_id: int = Field(foreign_key="user.id")

class LinkOrderUpdate(SQLModel):
    id: int
    order: int