from sqlmodel import Field, Session, SQLModel, create_engine, select
from database.postgres import create_db_and_tables, engine
from models.apps_ratings import Apps_Ratings
from models.user_model import User
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List


class RatingInfo(BaseModel):
    comment: str
    username: str
    user_id: int
    app_rating_id: int


def handle_get_app_ratings(app_id: int) -> List[RatingInfo]:
    with Session(engine) as session:
        statement = (
            select(
                Apps_Ratings.comment,
                User.username,
                Apps_Ratings.user_id,
                Apps_Ratings.id,
            )
            .join(User, User.id == Apps_Ratings.user_id, isouter=True)
            .where(Apps_Ratings.app_id == app_id)
        )

        results = session.exec(statement)

        # Convert results to RatingInfo objects
        rating_infos = [
            RatingInfo(
                comment=result[0],
                username=result[1],
                user_id=result[2],
                app_rating_id=result[3],
            )
            for result in results
        ]

        return rating_infos


def post_apps_ratings(app_ratings: Apps_Ratings):
    with Session(engine) as session:
        session.add(app_ratings)
        session.commit()
        session.refresh(app_ratings)
        return app_ratings


def handle_delete_app_rating(app_id: int):
    with Session(engine) as session:
        statement = select(Apps_Ratings).where(Apps_Ratings.id == app_id)
        results = session.exec(statement)
        app = results.one()

        session.delete(app)
        session.commit()

        statement = select(Apps_Ratings).where(Apps_Ratings.id == app_id)
        results = session.exec(statement)
        app = results.first()

        if app is None:
            return "successfully deleted"
