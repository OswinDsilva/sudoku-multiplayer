from pydantic import BaseModel
from pydantic.functional_validators import field_validator


class Board(BaseModel):
    board: list[list[int]]
    completed: bool
    cells_filled: int

    @field_validator("board")
    @classmethod
    def enforce_9x9(cls, v: list[list[int]]) -> list[list[int]]:
        if len(v) != 9 or all(len(row) != 9 for row in v):
            raise ValueError("Not 9x9")
        return v

    def validate_board(self) -> bool:
        return False

    def validate_move(self, row: int, col:int , value: int) -> bool:
        return False

    def fill_cell(self, row: int, col: int , value: int ):
        if not self.validate_move(row, col, value):
            pass
