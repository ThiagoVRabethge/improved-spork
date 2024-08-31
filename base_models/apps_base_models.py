from pydantic import BaseModel


class Get_All_Apps(BaseModel):
    id: int
    name: str
    description: str
    link: str
    username: str
