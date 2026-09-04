import uuid

from fastapi import WebSocket
from pydantic import BaseModel

from ..models import Board
from ..schema import Event


class Room(BaseModel):
    room_id: uuid.UUID = uuid.uuid4()
    room_size: int
    board: Board = Board()
    active_connections: list[WebSocket] = []

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
