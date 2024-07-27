from fastapi import FastAPI, HTTPException
from models.user_model import User
from sqlmodel import Field, Session, SQLModel, create_engine, select
from database.postgres import create_db_and_tables, engine
import re
from passlib.hash import pbkdf2_sha256


def login(user: User):
    with Session(engine) as session:
        statement = select(User).where(User.username == user.username)
        results = session.exec(statement)
        for db_user in results:
            if not pbkdf2_sha256.verify(user.password, db_user.password):
                raise HTTPException(status_code=400, detail="Wrong password")
            else:
                return {"id": db_user.id, "username": db_user.username}


def post_user(user: User):
    if not re.match(r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{8,}$", user.password):
        raise HTTPException(status_code=400, detail="Password too weak")

    user.password = pbkdf2_sha256.hash(user.password)

    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
