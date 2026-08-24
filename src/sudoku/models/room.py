from pydantic import BaseModel
from pydantic.functional_validators import field_validator

from .mode import Mode


class Room(BaseModel):
    room_id: str
    room_size: int
    difficulty: str
    mode: Mode

    @field_validator("difficulty")
    @classmethod
    def convert_to_lowercase(cls, v: str) -> str:
        return v.lower();

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        if v not in ("easy", "medium", "hard"):
            raise ValueError("Invalid difficulty")
        return v

    def select_mode(self):
        pass
