from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from models import Users, Users_Habits

from passlib.context import CryptContext

import re

from fastapi import FastAPI, HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_users():
    with Session(engine) as session:
        users = session.exec(select(Users)).all()
        return users
    

def get_user_by_id(id: int):
    with Session(engine) as session:
        statement = select(Users).where(Users.id == id)
        results = session.exec(statement)
        for user in results:
            return user


def post_user(user: Users):
    #  (?=.*[A-Z]) ensures there’s at least one uppercase letter.
    # (?=.*[0-9]) requires at least one digit.
    # (?=.*[^a-zA-Z0-9]) checks for at least one special character.
    # .{8,} enforces a minimum length of 8 characters.

    if not re.match(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{8,}$', user.password):
        raise HTTPException(status_code=404, detail="Password too weak")
    
    user.password = pwd_context.hash(user.password) 
    
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_users_habits(user_id: int):
        with Session(engine) as session:
            statement = select(Users_Habits).where(Users_Habits.user_id == user_id)
            results = session.exec(statement)
            return results.all()
        

def post_users_habits(users_habits: Users_Habits):
        with Session(engine) as session:
            session.add(users_habits)
            session.commit()
            session.refresh(users_habits)
            return users_habits
