import re

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

from base_models.user_base_models import SignInUpParams, SignInUpResponse
from database.postgres import create_db_and_tables, engine
from models.user_model import User


class Put_User_BaseModel(BaseModel):
    user_id: int
    icon: str
    about_me: str


def handle_get_user_profile(user_id: int):
    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        results = session.exec(statement)
        db_user = results.one()
        return {
            "icon": db_user.icon,
            "username": db_user.username,
            "about_me": db_user.about_me,
        }


def handle_put_user(user: Put_User_BaseModel):
    with Session(engine) as session:
        statement = select(User).where(User.id == user.user_id)
        results = session.exec(statement)
        db_user = results.one()

        db_user.icon = user.icon
        db_user.about_me = user.about_me

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user
