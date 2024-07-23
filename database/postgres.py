from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from models.user_model import User
import os
from dotenv import load_dotenv

load_dotenv()

pg_url = os.environ.get("PG_URL")
engine = create_engine(pg_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
