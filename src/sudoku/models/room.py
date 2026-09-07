import uuid

from fastapi import WebSocket

from ..models import Board
from ..schema import Event


class Room:
    def __init__(self, room_size:int) :
        self.room_id: uuid.UUID = uuid.uuid4()
        self.room_size: int = room_size
        self.board: Board = Board()
        self.active_connections: list[WebSocket] = []
        self.game_state: str = "not-started"

    async def connect_socket(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect_socket(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, event: Event):
        for connection in self.active_connections:
            await connection.send_json(event.model_dump())

    def set_board(self, board: Board):
        self.board = board
