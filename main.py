from fastapi import FastAPI

from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from models import Hero, Users

from controllers import get_users, post_user

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes


@app.get("/users")
def read_users():
    return get_users()


@app.post("/users")
def create_user(user: Users):
    return post_user(user)
