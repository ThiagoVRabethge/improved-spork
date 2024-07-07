from fastapi import FastAPI

from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from models import Users, Users_Habits

from controllers import get_users, get_user_by_id, post_user, post_users_habits, get_users_habits

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

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


@app.get("/users")
def read_users():
    return get_users()


@app.get("/users/{id}")
def user_by_id(id):
    return get_user_by_id(id)


@app.post("/users")
def create_user(user: Users):
    return post_user(user)


@app.get("/users_habits/{user_id}")
def read_users_habits(user_id):
    return get_users_habits(user_id)

@app.post("/users_habits")
def create_users_habits(users_habits: Users_Habits):
    return post_users_habits(users_habits)
