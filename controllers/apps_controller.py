from sqlmodel import Field, Session, SQLModel, create_engine, select

from database.postgres import engine, create_db_and_tables

from models.apps_model import Apps

from fastapi import FastAPI, HTTPException

from models.user_model import User

from pydantic import BaseModel

# from base_models.apps_base_models import Get_All_Apps

from typing import List

# class Get_All_Apps(BaseModel):
#     app_name: str
#     app_description: str
#     username: str


class Get_All_Apps(BaseModel):
    id: int
    name: str
    description: str
    link: str
    username: str


def handle_get_apps() -> List[Get_All_Apps]:
    with Session(engine) as session:
        statement = select(
            Apps.user_id,
            Apps.name,
            Apps.description,
            Apps.link,
            User.username,
        ).join(User, User.id == Apps.user_id, isouter=True)

        results = session.exec(statement)

        all_apps = [
            Get_All_Apps(
                id=result[0],
                name=result[1],
                description=result[2],
                link=result[3],
                username=result[4],
            )
            for result in results
        ]

        return all_apps


def get_apps_by_user(user_id: int):
    with Session(engine) as session:
        statement = select(Apps).where(Apps.user_id == user_id)
        results = session.exec(statement)
        return results.all()


def post_app(app: Apps):
    with Session(engine) as session:
        session.add(app)
        session.commit()
        session.refresh(app)
        return app


def put_app(app_id: int, app: Apps):
    with Session(engine) as session:
        statement = select(Apps).where(Apps.id == app_id)
        results = session.exec(statement)
        db_app = results.one()

        db_app.name = app.name
        db_app.description = app.description
        db_app.link = app.link

        session.add(db_app)
        session.commit()
        session.refresh(db_app)

        return db_app


def delete_app(app_id: int):
    with Session(engine) as session:
        statement = select(Apps).where(Apps.id == app_id)
        results = session.exec(statement)
        app = results.one()

        session.delete(app)
        session.commit()

        statement = select(Apps).where(Apps.id == app_id)
        results = session.exec(statement)
        app = results.first()

        if app is None:
            return "successfully deleted"
