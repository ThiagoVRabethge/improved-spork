from fastapi.responses import JSONResponse
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from database.postgres import create_db_and_tables, engine
from models.user_model import User


def handle_register(user: User) -> User:
    with Session(engine) as session:
        # Verifica se o usuário já existe
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Nome de usuário já existe")

        # Hash da senha
        user.password = pbkdf2_sha256.hash(user.password)

        try:
            session.add(user)
            session.commit()
            session.refresh(user)
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=400, detail="Erro ao criar usuário")

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
        statement = select(User).where(User.username == user.username).limit(1)
        db_user = session.exec(statement).first()
        
        if not db_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        if not pbkdf2_sha256.verify(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Senha incorreta")
        
        return JSONResponse({
            "id": db_user.id,
            "username": db_user.username,
            "icon": db_user.icon,
            "about_me": db_user.about_me,
        })
