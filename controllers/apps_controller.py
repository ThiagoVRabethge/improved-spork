from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from models.apps_model import Apps

from fastapi import FastAPI, HTTPException


def get_apps():
    with Session(engine) as session:
        statement = select(Apps)
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
