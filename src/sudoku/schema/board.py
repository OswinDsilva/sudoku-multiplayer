from pydantic import BaseModel, Field
from typing_extensions import Literal


class CellFillRequest(BaseModel):
    row: int = Field(ge=0, lt=9)
    col: int = Field(ge=0, lt=9)
    val: int = Field(gt=0, le=9)


class CellClearRequest(BaseModel):
    row: int = Field(ge=0, lt=9)
    col: int = Field(ge=0, lt=9)


class UpdateBoardRequest(BaseModel):
    board: list[list[int]]
    gameState: Literal["not-started", "started"]
