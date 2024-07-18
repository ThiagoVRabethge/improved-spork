from sqlmodel import Field, Session, SQLModel, create_engine, select

import os

from dotenv import load_dotenv

load_dotenv()

sqlite_file_name = os.environ.get("DATABASE_NAME")

sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
