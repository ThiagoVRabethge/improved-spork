from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from database.postgres import create_db_and_tables, engine
from models.user_model import User
from controllers.users_controller import (
    login,
    post_user,
    handle_get_user_profile,
    handle_put_user,
)
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from controllers.apps_controller import (
    get_apps,
    get_apps_by_user,
    post_app,
    put_app,
    delete_app,
)
from models.apps_model import Apps
import timeout_decorator
from models.apps_ratings import Apps_Ratings
from controllers.apps_ratings_controller import (
    post_apps_ratings,
    handle_get_app_ratings,
)
from pydantic import BaseModel

load_dotenv()

app = FastAPI()


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


# docs route


@app.get("/")
def docs():
    return {"docs": "access /docs to see"}


# auth routes


@timeout_decorator.timeout(1)
@app.post("/sign_in")
def sign_in(user: User):
    return login(user)


@app.post("/sign_up")
def sign_up(user: User):
    return post_user(user)


@app.get("/users/{user_id}/profile")
def get_user_profile(user_id: int):
    return handle_get_user_profile(user_id)


class Put_User_BaseModel(BaseModel):
    user_id: int
    icon: str
    about_me: str


@app.put("/users")
def put_user(user: Put_User_BaseModel):
    return handle_put_user(user)


# apps routes


@app.get("/apps")
def read_all_apps():
    return get_apps()


@app.get("/users/{user_id}/apps")
def read_user_apps(user_id: int):
    return get_apps_by_user(user_id)


@app.post("/apps")
def add_app(app: Apps):
    return post_app(app)


@app.put("/apps/{app_id}")
def update_app(app_id: int, app: Apps):
    return put_app(app_id, app)


@app.delete("/apps/{app_id}")
def exclude_app(app_id: int):
    return delete_app(app_id)


@app.get("/apps_ratings/{app_id}")
def get_app_ratings(app_id: int):
    return handle_get_app_ratings(app_id)


@app.post("/apps_ratings")
def app_ratings(apps_ratings: Apps_Ratings):
    return post_apps_ratings(apps_ratings)
