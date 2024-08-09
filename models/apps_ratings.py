from sqlmodel import Field, Session, SQLModel, create_engine, select


class Apps_Ratings(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    app_id: int
    comment: str
