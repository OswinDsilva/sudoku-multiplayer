from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from ..exceptions import HintCellRemovalError, InvalidMoveError
from ..models import Board
from ..schema import CellClearRequest, CellFillRequest

router = APIRouter(prefix="/boards",tags=["boards"])

current_board: Board = Board()

@router.post("/start")
def create_board():
    current_board.generate_board()
    return {
        "board": current_board.board,
    }

@router.get("/board")
def get_board():
    return {
        "board": current_board.board
    }

@router.post("/fill", status_code=status.HTTP_201_CREATED)
def fill_board_cell(req: CellFillRequest):
    row = req.row
    col = req.col
    val = req.val
    try:
        current_board.fill_cell(row, col, val)

        if current_board.cells_filled == 81:
            current_board.completed = True
    except InvalidMoveError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Value exists in box, column or row")
    except HintCellRemovalError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot edit a hint cell")

    return {
        "board": current_board.board,
        "completed": current_board.completed
    }

@router.delete("/clear")
def clear_board_cell(req: CellClearRequest):
    row = req.row
    col = req.col

    try:
        current_board.clear_cell(row, col)
    except HintCellRemovalError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot clear a hint cell")

    return {
        "board": current_board.board
    }
