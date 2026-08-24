from pydantic import BaseModel

from .mode import Mode


class Room(BaseModel):
    room_id: str
    mode: Mode
