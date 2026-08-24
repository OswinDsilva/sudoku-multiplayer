from pydantic import BaseModel
from pydantic.functional_validators import field_validator


class Mode(BaseModel):
    difficulty: str

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

class SyncMode(Mode):
    pass

class IndividualMode(Mode):
    pass
