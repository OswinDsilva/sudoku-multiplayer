from pydantic import BaseModel, field_validator

from .board import CellClearRequest, CellFillRequest, UpdateBoardRequest


class Event(BaseModel):
    type: str
    body: CellClearRequest | CellFillRequest | UpdateBoardRequest

    @field_validator('type')
    @classmethod
    def valid_event(cls, v: str) -> str:
        if v not in ["fill_cell","clear_cell","update_board"]:
            raise ValueError("Not a valid value for type")
        return v
