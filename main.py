from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from database.postgres import create_db_and_tables, engine
from models.user_model import User
from controllers.users_controller import (
    handle_sign_in,
    handle_sign_up,
    handle_get_user_profile,
    handle_put_user,
)
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from controllers.apps_controller import (
    handle_get_apps,
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
    handle_delete_app_rating,
    handle_put_app_rating,
)
from pydantic import BaseModel
from base_models.put_app_rating import Put_App_Rating_BaseModel
from passlib.hash import pbkdf2_sha256
from fastapi.responses import JSONResponse
import os
import shutil
from fastapi.staticfiles import StaticFiles
from typing import Optional
from base_models.user_base_models import SignInUpParams

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


@app.get("/")
def docs():
    return {"docs": "access /docs", "redoc": "access /redoc"}


@app.post("/sign_in")
async def sign_in(user: SignInUpParams):
    return await handle_sign_in(user)


@app.post("/sign_up")
async def sign_up(user: SignInUpParams):
    return await handle_sign_up(user)


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


@app.get("/apps")
def get_apps():
    return handle_get_apps()


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


@app.put("/apps_ratings")
def put_app_rating(app_rating: Put_App_Rating_BaseModel):
    return handle_put_app_rating(app_rating)


@app.delete("/apps_ratings/{app_rating_id}")
def delete_app_rating(app_rating_id: int):
    return handle_delete_app_rating(app_rating_id)


UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_FOLDER)), name="uploads")


@app.post("/upload/{user_id}/{about_me}")
async def upload_file(user_id: str, about_me: str, file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, f"{user_id}_{file.filename}")

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        results = session.exec(statement)
        db_user = results.one()

        db_user.icon = f"{user_id}_{file.filename}"
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


@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Verificar se o arquivo existe
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
