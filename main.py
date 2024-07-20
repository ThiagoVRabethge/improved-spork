from fastapi import FastAPI

from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from fastapi.middleware.cors import CORSMiddleware

from models.apps_model import Apps

from controllers.apps_controller import get_apps, post_app, delete_app, put_app

from models.users_model import Users

from controllers.users_controller import post_user, login, get_user_apps

import os

from dotenv import load_dotenv

app = FastAPI()


load_dotenv()


origins = [os.environ.get("LOCALHOST"), os.environ.get("PRODUCTION_URL")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_docs():
    return {"Documentation": "Visit the /docs endpoint to see"}


@app.post("/login")
def sign_in(user: Users):
    return login(user)


@app.post("/users")
def create_user(user: Users):
    return post_user(user)


@app.get("/users/{user_id}/apps")
def read_user_apps(user_id: int):
    return get_user_apps(user_id)


@app.get("/apps")
def read_all_apps():
    return get_apps()


@app.post("/apps")
def add_app(app: Apps):
    return post_app(app)


@app.put("/apps/{app_id}")
def update_app(app_id: int, app: Apps):
    return put_app(app_id, app)


@app.delete("/apps/{app_id}")
def exclude_app(app_id: int):
    return delete_app(app_id)


@app.get("/test")
def test_endpoint():
    return "test"