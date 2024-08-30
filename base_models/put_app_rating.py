from pydantic import BaseModel


class Put_App_Rating_BaseModel(BaseModel):
    app_rating_id: int
    new_rating: str
