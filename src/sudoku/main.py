from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status":"Running"}

@app.get("/health")
def health_check():
    return {"status":"OK"}
