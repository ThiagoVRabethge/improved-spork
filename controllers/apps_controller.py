from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from models.apps_model import Apps


def post_app(app: Apps):
    with Session(engine) as session:
        session.add(app)
        session.commit()
        session.refresh(app)
        return app
