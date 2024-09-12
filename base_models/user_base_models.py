from pydantic import BaseModel
from typing import Optional


class SignInUpParams(BaseModel):
    username: str
    password: str


class SignInUpResponse(BaseModel):
    id: int
    username: str
    icon: Optional[str] = None
    about_me: Optional[str] = None
