from fastapi import FastAPI
from app.routers import auth,room
from app.dependencies.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from app.routers.ws_chat import router as ws_chat_router
import os

app = FastAPI(title="FastAPI Chat App")

# Get allowed origins from environment or use defaults
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    origins = [origin.strip() for origin in allowed_origins_env.split(",")]
else:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Chat App!"}


app.include_router(auth.router)
app.include_router(room.router)
app.include_router(ws_chat_router)
