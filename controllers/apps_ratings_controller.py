from sqlmodel import Field, Session, SQLModel, create_engine, select
from database.postgres import create_db_and_tables, engine
from models.apps_ratings import Apps_Ratings


def post_apps_ratings(app_ratings: Apps_Ratings):
    with Session(engine) as session:
        session.add(app_ratings)
        session.commit()
        session.refresh(app_ratings)
        return app_ratings
