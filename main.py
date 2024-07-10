from fastapi import FastAPI

from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from models import Users, Users_Habits

from controllers import post_user, login

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://potential-funicular.onrender.com",
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


@app.post("/login")
def sign_in(user: Users):
    return login(user)


@app.post("/users")
def create_user(user: Users):
    return post_user(user)
