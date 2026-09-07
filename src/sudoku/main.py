from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import board, room

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:8000",
    "http://localhost:5000",
    "http://frontend:80",
    "*.trycloudflare.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(board.router)
app.include_router(room.router)

@app.get("/")
def read_root():
    return {"status":"Running"}

@app.get("/health")
def health_check():
    return {"status":"OK"}
