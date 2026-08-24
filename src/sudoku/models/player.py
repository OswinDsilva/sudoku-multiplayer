from pydantic import BaseModel


class Player(BaseModel):
    user_id : str
    user_name : str
