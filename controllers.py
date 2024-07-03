from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import engine, create_db_and_tables

from models import Users


def get_users():
    with Session(engine) as session:
        users = session.exec(select(Users)).all()
        return users
    

def get_user_by_id(id: int):
    with Session(engine) as session:
        statement = select(Users).where(Users.id == id)
        results = session.exec(statement)
        for user in results:
            return user


def post_user(user: Users):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
