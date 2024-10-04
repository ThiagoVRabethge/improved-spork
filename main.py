import os
import shutil
import uuid
from typing import Optional

import timeout_decorator
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

from base_models.put_app_rating import Put_App_Rating_BaseModel
from controllers.apps_controller import (
    delete_app,
    get_apps_by_user,
    handle_get_apps,
    post_app,
    put_app,
)
from controllers.apps_ratings_controller import (
    handle_delete_app_rating,
    handle_get_app_ratings,
    handle_put_app_rating,
    post_apps_ratings,
)
from controllers.auth_controller import handle_login, handle_register
from controllers.users_controller import handle_get_user_profile
from database.postgres import create_db_and_tables, engine
from middlewares.add_cors_middleware import add_cors_middleware
from models.apps_model import Apps
from models.apps_ratings import Apps_Ratings
from models.user_model import User
from services.firebase import initialize_firebase

app = FastAPI()

bucket = initialize_firebase()


add_cors_middleware(app)

# start server


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# root


@app.get("/")
def docs():
    return {"docs": "access /docs to see", "redoc": "access /redoc to see"}


# auth


@app.post("/register")
def register(user: User):
    return handle_register(user)


@app.post("/login")
def login(user: User):
    return handle_login(user)


# user


@app.get("/users/{user_id}/profile")
def get_user_profile(user_id: int):
    return handle_get_user_profile(user_id)


@app.get("/users/{user_id}/apps")
def read_user_apps(user_id: int):
    return get_apps_by_user(user_id)


@app.post("/users/{user_id}/profile/{about_me}")
async def upload_image(user_id: int, about_me: str, file: UploadFile = File(...)):
    try:
        blob_name = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"

        blob = bucket.blob(blob_name)

        blob.upload_from_file(file.file, content_type=file.content_type)

        blob.make_public()

        url = blob.public_url

        with Session(engine) as session:
            statement = select(User).where(User.id == user_id)
            results = session.exec(statement)

            db_user = results.one()

            db_user.icon = url
            db_user.about_me = about_me

            session.add(db_user)
            session.commit()
            session.refresh(db_user)

            return JSONResponse(
                {
                    "id": db_user.id,
                    "username": db_user.username,
                    "icon": db_user.icon,
                    "about_me": db_user.about_me,
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")


# apps


@app.get("/apps")
def get_apps():
    return handle_get_apps()


@app.post("/apps")
def add_app(app: Apps):
    return post_app(app)


@app.put("/apps/{app_id}")
def update_app(app_id: int, app: Apps):
    return put_app(app_id, app)


@app.delete("/apps/{app_id}")
def exclude_app(app_id: int):
    return delete_app(app_id)


# apps ratings


@app.get("/apps_ratings/{app_id}")
def get_app_ratings(app_id: int):
    return handle_get_app_ratings(app_id)


@app.post("/apps_ratings")
def app_ratings(apps_ratings: Apps_Ratings):
    return post_apps_ratings(apps_ratings)


@app.put("/apps_ratings")
def put_app_rating(app_rating: Put_App_Rating_BaseModel):
    return handle_put_app_rating(app_rating)


@app.delete("/apps_ratings/{app_rating_id}")
def delete_app_rating(app_rating_id: int):
    return handle_delete_app_rating(app_rating_id)


if __name__ = "__main__":
import uvicorn

uvicorn.run("main.py")
