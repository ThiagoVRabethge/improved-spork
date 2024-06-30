from typing import Union

from fastapi import FastAPI

from controllers import users_controller

from schemas.user import user

app = FastAPI()

@app.get("/")
def root():
    return {"Saiba mais": "Acesse http://localhost:8000/docs para saber mais"}

@app.get("/users")
def users():
    return users_controller.get_user()

@app.get("/users/{user_id}")
def user_by_id(user_id: int):
    return users_controller.get_user_by_id(user_id)

@app.post("/users")
def new_user(user: user):
    return users_controller.post_user(user)