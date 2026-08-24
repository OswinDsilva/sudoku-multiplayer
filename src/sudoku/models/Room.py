from pydantic import BaseModel


class Room(BaseModel):
    room_id: str
    mode: Mode
