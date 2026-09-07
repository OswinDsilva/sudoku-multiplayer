from typing import Literal

from pydantic import BaseModel, Field


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
