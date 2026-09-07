import uuid
from copy import deepcopy

from fastapi import WebSocket, WebSocketDisconnect, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from ..models import Room
from ..schema import CellClearRequest, CellFillRequest, Event, UpdateBoardRequest

router = APIRouter(prefix="/room", tags=["room"])

rooms_mapping: dict[uuid.UUID, Room] = {}

async def handle_event_routing(event: Event, id: uuid.UUID):
    room = rooms_mapping[id]
    data = event.body
    payload = {}
    if event.type == "fill_cell":
        data = CellFillRequest.model_validate(data)
        room.board.fill_cell(data.row, data.col, data.val)

    elif event.type == "clear_cell":
        data = CellClearRequest.model_validate(data)
        room.board.clear_cell(data.row, data.col)

    elif event.type == "update_board":
        data = UpdateBoardRequest.model_validate(data)
        room.board.board = data.board

    elif event.type == "start_game":
        if room.game_state == "not-started":
            room.game_state = "started"
            room.board.generate_board()


    payload =  Event.model_validate({
        "type": "update_board",
        "body": {
            "board": deepcopy(room.board.board),
            "gameState": room.game_state
        }
    })
    await room.broadcast(payload)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_room(room_size: int) -> dict:
    room = Room(room_size=room_size)
    rooms_mapping[room.room_id] = room

    return {
        "room_id": room.room_id
    }

# id as a query parameter
@router.get("/join")
async def join_room(id: uuid.UUID) -> dict:
    if id not in rooms_mapping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    return {
        "room_id": id
    }

@router.websocket("/{id}")
async def game_room(id: uuid.UUID, websocket: WebSocket):
    room = rooms_mapping[id]
    await room.connect_socket(websocket=websocket)
    try:
        while True:
            data = await websocket.receive_json()
            event = Event.model_validate(data)

            await handle_event_routing(event, room.room_id)

    except WebSocketDisconnect:
        room.disconnect_socket(websocket)
        print("Connection terminated")
