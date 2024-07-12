from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from models import Users, Users_Habits, Apps

from passlib.context import CryptContext

import re

from fastapi import FastAPI, HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def login(user: Users):
    with Session(engine) as session:
        statement = select(Users).where(Users.username == user.username)
        results = session.exec(statement)
        for db_user in results:
            if not pwd_context.verify(user.password, db_user.password):
                raise HTTPException(status_code=400, detail="Wrong password")
            else:
                return db_user.username


def post_user(user: Users):
    if not re.match(r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{8,}$", user.password):
        raise HTTPException(status_code=400, detail="Password too weak")

    user.password = pwd_context.hash(user.password)

    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user_apps(user_id: int):
    with Session(engine) as session:
        statement = select(Apps).where(Apps.user_id == user_id)
        results = session.exec(statement)
        return results.all()


def post_app(app: Apps):
    with Session(engine) as session:
        session.add(app)
        session.commit()
        session.refresh(app)
        return app
