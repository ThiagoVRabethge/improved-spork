from sqlmodel import Field, Session, SQLModel, create_engine, select


class Apps_Ratings(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    app_id: int = Field(default=None, foreign_key="apps.id")
    comment: str
