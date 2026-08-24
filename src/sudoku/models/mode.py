from pydantic import BaseModel

from .board import Board
from .player import Player


class Mode(BaseModel):
    time: float

    def get_board(self, p: Player):
        pass

    def make_move(self, p:Player):
        pass

class SyncMode(Mode):
    pass

class RaceMode(Mode):
    board_player_mapping: dict[str, Board]
