from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import UniqueConstraint
from typing import Optional


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("username"),)
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str
    icon: Optional[str] = Field(default=None)
    about_me: Optional[str] = Field(default=None)
