import uuid
from copy import deepcopy

from fastapi import WebSocket, WebSocketDisconnect, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
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

    payload =  Event.model_validate({
        "type": "update_board",
        "body": deepcopy(room.board.board)
    })
    await room.broadcast(payload)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_room(room_size: int) -> RedirectResponse:
    room = Room(room_size=room_size)
    rooms_mapping[room.room_id] = room

    return RedirectResponse(
        url=f"/room/{room.room_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )

# id as a query parameter
@router.get("/join")
async def join_room(id: uuid.UUID) -> RedirectResponse:
    if id not in rooms_mapping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    return RedirectResponse(
        url=f"/room/{id}",
        status_code=status.HTTP_303_SEE_OTHER
    )

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
