from fastapi.responses import JSONResponse
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

from database.postgres import create_db_and_tables, engine
from models.user_model import User


def handle_register(user: User) -> User:
    user.password = pbkdf2_sha256.hash(user.password)

    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return JSONResponse(
            {
                "id": user.id,
                "username": user.username,
                "icon": user.icon,
                "about_me": user.about_me,
            }
        )


def handle_login(user: User) -> User:
    with Session(engine) as session:
        statement = select(User).where(User.username == user.username)

        results = session.exec(statement)

        for db_user in results:
            if not pbkdf2_sha256.verify(user.password, db_user.password):
                raise HTTPException(status_code=400, detail="Wrong password")
            else:
                return JSONResponse(
                    {
                        "id": db_user.id,
                        "username": db_user.username,
                        "icon": db_user.icon,
                        "about_me": db_user.about_me,
                    }
                )
