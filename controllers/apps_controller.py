from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from models.apps_model import Apps


def post_app(app: Apps):
    with Session(engine) as session:
        session.add(app)
        session.commit()
        session.refresh(app)
        return app


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
