from pydantic import BaseModel, field_validator

from .board import CellClearRequest, CellFillRequest, UpdateBoardRequest


class Event(BaseModel):
    type: str
    body: CellClearRequest | CellFillRequest | UpdateBoardRequest | None = None

    @field_validator('type')
    @classmethod
    def valid_event(cls, v: str) -> str:
        if v not in ["fill_cell","clear_cell","update_board","start_game","retrieve_state"]:
            raise ValueError("Not a valid value for type")
        return v
