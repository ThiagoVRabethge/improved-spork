from fastapi import FastAPI

from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from models import Users

from controllers import get_users, get_user_by_id, post_user

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/users")
def read_users():
    return get_users()


@app.get("/users/{id}")
def user_by_id(id):
    return get_user_by_id(id)


@app.post("/users")
def create_user(user: Users):
    return post_user(user)
