from fastapi import FastAPI

from .api import board

app = FastAPI()

app.include_router(board.router)

@app.get("/")
def read_root():
    return {"status":"Running"}

@app.get("/health")
def health_check():
    return {"status":"OK"}
