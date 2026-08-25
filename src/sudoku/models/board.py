import random
from typing import Any
import copy

from pydantic import BaseModel, Field
from pydantic.functional_validators import field_validator


class Board(BaseModel):
    board: list[list[int]] = Field(
        default_factory=lambda:[[0 for _ in range(9)] for _ in range(9)]
    )
    completed: bool = False
    cells_filled: int = 0
    sol_found: bool = False
    _hints: list[list[int]]
    _rows: list[list[bool]]
    _cols: list[list[bool]]
    _squares: list[list[bool]]

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)
        self._rows = [[False for _ in range(9)] for _ in range(9)]
        self._cols = [[False for _ in range(9)] for _ in range(9)]
        self._squares = [[False for _ in range(9)] for _ in range(9)]

    @field_validator("board")
    @classmethod
    def enforce_9x9(cls, v: list[list[int]]) -> list[list[int]]:
        if len(v) != 9 or all(len(row) != 9 for row in v):
            raise ValueError("Not 9x9")
        return v

    def _set_cell(self, i:int, j:int, num:int):
        square_idx = (i // 3) * 3 + (j // 3)
        self._rows[i][num-1] = True
        self._cols[j][num-1] = True
        self._squares[square_idx][num-1] = True
        self.board[i][j] = num
        self.cells_filled += 1

    def _del_cell(self, i:int, j:int, num: int):
        square_idx = (i // 3) * 3 + (j // 3)
        self.board[i][j] = 0
        self._rows[i][num-1] = False
        self._cols[j][num-1] = False
        self._squares[square_idx][num-1] = False
        self.cells_filled -= 1

    def generate_board(self):
        _ = self._generate_grid(0,0)
        self._destroy_cells()
        self._hints = copy.deepcopy(self.board)

    def _generate_grid(self,i: int, j: int) -> bool:
        if i == 9:
            return True
        if j == 9:
            return self._generate_grid(i+1, 0)

        if self.board[i][j] != 0:
            return self._generate_grid(i, j+1)

        numbers = [1,2,3,4,5,6,7,8,9]
        random.shuffle(numbers)
        while numbers:
            num = numbers.pop()
            if self._validate_move(i, j, num):
                continue
            self._set_cell(i, j, num)
            if self._generate_grid(i, j+1):
                return True
            self._del_cell(i, j, num)

        return False

    def _destroy_cells(self):
        upper_bound = 45
        lower_bound = 35

        itr = 0
        while (lower_bound < self.cells_filled < upper_bound and itr % 9 != 0) or self.cells_filled > upper_bound:
            if(itr > 81):
                break
            i = random.randint(0, 8)
            j = random.randint(0, 8)

            if self.board[i][j] == 0:
                itr +=  1
                continue

            val = self.board[i][j]
            self._del_cell(i,j,val)
            self.sol_found = False
            if not self._uniquely_solvable(0, 0):
                self._set_cell(i,j,val)

            itr += 1

    def _validate_move(self, row: int, col:int , value: int) -> bool:
        sq_idx = (row // 3) * 3 + (col // 3)
        return self._rows[row][value-1] or self._cols[col][value-1] or self._squares[sq_idx][value-1]

    def fill_cell(self, row: int, col: int , value: int ):
        # handle at API layer later
        if(row >= 9 or row < 0 or col >= 9 or col < 0 or value < 1 or value > 9):
            raise IndexError("Beyond bounds")

        if self.board[row][col] == value:
            return

        if self._validate_move(row, col, value):
            raise ValueError("Conflicting")

        if self.board[row][col] != 0:
            self.clear_cell(row, col)

        self._set_cell(row, col, value)

    def clear_cell(self, row: int, col: int):
        # handle at API layer later
        if(row >= 9 or row < 0 or col >= 9 or col < 0):
            raise IndexError("Beyond bounds")

        if self._hints[row][col] != 0:
            raise ValueError("Cannot clear initial hints")

        self._del_cell(row, col, self.board[row][col])

    def _uniquely_solvable(self,i: int, j: int) -> bool:
        if i == 9:
            if self.sol_found:
                return False
            else:
                self.sol_found = True
                return True

        if j == 9:
            return self._uniquely_solvable(i+1, 0)

        if self.board[i][j] != 0:
            return self._uniquely_solvable(i, j+1)

        for num in range(1,9+1):
            if self._validate_move(i, j, num):
                continue

            self._set_cell(i, j, num)

            if not self._uniquely_solvable(i, j+1):
                self._del_cell(i, j, num)
                return False

            self._del_cell(i, j, num)

        return True
