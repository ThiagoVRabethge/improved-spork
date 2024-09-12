from pydantic import BaseModel
from typing import Optional


class SignInParams(BaseModel):
    username: str
    password: str


class SignInResponse(BaseModel):
    id: int
    username: str
    icon: Optional[str] = None
    about_me: Optional[str] = None
