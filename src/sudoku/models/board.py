import random

from pydantic import BaseModel
from pydantic.functional_validators import field_validator


class Board(BaseModel):
    board: list[list[int]]
    completed: bool
    cells_filled: int
    sol_found: bool = False
    _rows: list[list[bool]] = [[False for _ in range(9)] for _ in range(9)]
    _cols: list[list[bool]] = [[False for _ in range(9)] for _ in range(9)]
    _squares: list[list[bool]] = [[False for _ in range(9)] for _ in range(9)]

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

    def _generate_grid(self,i: int, j: int) -> bool:
        if i == 9:
            return True
        if j == 9:
            return self._generate_grid(i+1, 0)

        if self.board[i][j] != 0:
            return self._generate_grid(i, j+1)
        for num in range(1,9+1):
            square_idx = (i // 3) * 3 + (j // 3)
            if self._rows[i][num-1] or self._cols[j][num-1] or self._squares[square_idx][num-1]:
                continue
            self._set_cell(i,j,num)
            if self._generate_grid(i, j+1):
                return True
            self._del_cell(i,j,num)
        return False

    def _destroy_cells(self):
        upper_bound = 45
        lower_bound = 35

        itr = 0
        print(self.cells_filled)
        while (lower_bound < self.cells_filled < upper_bound and itr % 9 != 0) or self.cells_filled > upper_bound:
            if(itr > 81):
                break
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            print(f"i:{i},j:{j},itr:{itr},cells_filled:{self.cells_filled}")

            if self.board[i][j] == 0:
                itr +=  1
                continue

            val = self.board[i][j]
            self._del_cell(i,j,val)
            if not self._uniquely_solvable(0, 0):
                self._set_cell(i,j,val)

            itr += 1

    def _validate_move(self, row: int, col:int , value: int) -> bool:
        sq_idx = (row // 3) * 3 + (col // 3)
        return self._rows[row][value-1] or self._cols[col][value-1] or self._squares[sq_idx][value-1]

    def fill_cell(self, row: int, col: int , value: int ):
        if not self._validate_move(row, col, value):
            pass

    # bugged , fix tomorrow
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

        can_continue = True
        for num in range(1,9+1):
            if self._validate_move(i,j, num):
                continue

            self._set_cell(i,j,num)

            can_continue = self._uniquely_solvable(i, j+1)

            self._del_cell(i,j,num)

            if not can_continue:
                return False

        return can_continue


    def _unique_solution(self, i:int, j:int) -> bool:
        if(i == 9):
            pass # return based on if a solution has been found or not

        if(j == 9):
            _ = self._unique_solution(i+1, 0)

        if(self.board[i][j] != 0):
            _ = self._unique_solution(i, j+1)

        for num in range(1, 9+1):
            if self._validate_move(i,j,num):
                continue

            self._set_cell(i, j, num)
            _ = self._unique_solution(i, j+1)
            self._del_cell(i, j, num)
