from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="FastAPI Chat App")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Chat App!"}


app.include_router(auth.router)
