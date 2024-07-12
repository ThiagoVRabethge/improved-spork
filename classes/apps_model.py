from sqlmodel import Field, Session, SQLModel, create_engine, select


class Apps(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    link: str
    user_id: int
