from sqlmodel import Field, Session, SQLModel, create_engine, select


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str = Field(index=True)


class Users_Habits(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    date: str
    checked: bool
    name: str


# class Apps(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     description: str
#     link: str
#     user_id: int
