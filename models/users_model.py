from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import UniqueConstraint


class Users(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("username"),)
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str = Field(index=True)
