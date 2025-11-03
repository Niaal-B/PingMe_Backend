from fastapi import FastAPI
from app.routers import auth
from app.dependencies.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI Chat App")

origins = [
    "http://localhost:5173",  
     "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],                # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],                # Authorization, Content-Type, etc.
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Chat App!"}


app.include_router(auth.router)
